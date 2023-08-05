#!/usr/bin/env python

from __future__ import print_function

import os
import itertools
import collections
import regex as re
import json
import gzip
import sys
import logging
import time
import multiprocessing
import tempfile
from io import BufferedReader, TextIOWrapper
from functools import partial
import toolz as tz

from .barcodes import (exact_barcode_filter, correcting_barcode_filter,
                       exact_sample_filter, correcting_sample_filter, exact_sample_filter2,
                       correcting_sample_filter2, umi_filter, append_uids, MutationHash)
import numpy as np
import scipy.io, scipy.sparse
import click

VERSION = "1.0.3"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BarcodeInfo = collections.namedtuple("BarcodeInfo", ["bamtag", "readprefix"])
BARCODEINFO = {"sample": BarcodeInfo(bamtag="XS", readprefix="SAMPLE"),
               "cellular": BarcodeInfo(bamtag="XC", readprefix="CELL"),
               "molecular": BarcodeInfo(bamtag="RX", readprefix="UMI")}

def open_gzipsafe(f):
    return gzip.open(f) if f.endswith(".gz") else open(f)

def safe_makedir(dname):
    """Make a directory if it doesn't exist, handling concurrent race conditions.
    """
    if not dname:
        return dname
    num_tries = 0
    max_tries = 5
    while not os.path.exists(dname):
        # we could get an error here if multiple processes are creating
        # the directory at the same time. Grr, concurrency.
        try:
            os.makedirs(dname)
        except OSError:
            if num_tries > max_tries:
                raise
            num_tries += 1
            time.sleep(2)
    return dname

def stream_fastq(file_handler):
    ''' Generator which gives all four lines if a fastq read as one string
    '''
    next_element = ''
    for i, line in enumerate(file_handler):
        next_element += line
        if i % 4 == 3:
            yield next_element
            next_element = ''

def read_fastq(filename):
    """
    return a stream of FASTQ entries, handling gzipped and empty files
    """
    if not filename:
        return itertools.cycle((None,))
    if filename == "-":
        filename_fh = sys.stdin
    elif filename.endswith('gz'):
        if is_python3:
            filename_fh = gzip.open(filename, mode='rt')
        else:
            filename_fh = BufferedReader(gzip.open(filename, mode='rt'))
    else:
        filename_fh = open(filename)
    return stream_fastq(filename_fh)

def read_cbhistogram(filename):
    if not filename:
        return None
    if filename.endswith('gz'):
#        filename_fh = BufferedReader(gzip.open(filename, mode='rt'))
        filename_fh = gzip.open(filename, mode='rt')
    else:
        filename_fh = open(filename)
    return filename_fh

def write_fastq(filename):
    """
    return a handle for FASTQ writing, handling gzipped files
    """
    if filename:
        if filename.endswith('gz'):
            filename_fh = gzip.open(filename, mode='wb')
        else:
            filename_fh = open(filename, mode='w')
    else:
        filename_fh = None
    return filename_fh

def stream_bamfile(sam, transcript=None):
    sam_file = open_bamfile(sam)
    if transcript:
        track = sam_file.fetch(transcript)
    else:
        track = sam_file.fetch(until_eof=True)
    return track

def open_bamfile(sam):
    from pysam import AlignmentFile
    sam_mode = 'r' if sam.endswith(".sam") else 'rb'
    return AlignmentFile(sam, mode=sam_mode)

def detect_alignment_annotations(queryalignment, tags=False):
    """
    detects the annotations present in a SAM file, inspecting either the
    tags or the query names and returns a set of annotations present
    """
    annotations = set()
    for k, v in BARCODEINFO.items():
        if tags:
            if queryalignment.has_tag(v.bamtag):
                annotations.add(k)
        else:
            if v.readprefix in queryalignment.qname:
                annotations.add(k)
    return annotations

def detect_fastq_annotations(fastq_file):
    """
    detects annotations preesent in a FASTQ file by examining the first read
    """
    annotations = set()
    queryread = tz.first(read_fastq(fastq_file))
    for k, v in BARCODEINFO.items():
        if v.readprefix in queryread:
            annotations.add(k)
    return annotations

def construct_transformed_regex(annotations):
    """
    construct a regex that matches possible fields in a transformed file
    annotations is a set of which keys in BARCODEINFO are present in the file
    """
    re_string = '.*'
    if "cellular" in annotations:
        re_string += ":CELL_(?P<CB>.*)"
    if "molecular" in annotations:
        re_string += ":UMI_(?P<MB>\w*)"
    if "sample" in annotations:
        re_string += ":SAMPLE_(?P<SB>\w*)"
    if re_string == ".*":
        logger.error("No annotation present on this file, aborting.")
        sys.exit(1)
    return re_string

@click.command()
@click.argument('transform', required=True)
@click.argument('fastq1', required=True)
@click.argument('fastq2', default=None, required=False)
@click.argument('fastq3', default=None, required=False)
@click.argument('fastq4', default=None, required=False)
@click.option('--keep_fastq_tags', default=False, is_flag=True)
@click.option('--separate_cb', is_flag=True,
              help="Keep dual index barcodes separate.")
@click.option('--demuxed_cb', default=None)
@click.option('--cores', default=1)
@click.option('--fastq1out', default=None)
@click.option('--fastq2out', default=None)
@click.option('--min_length', default=1, help="Minimum length of read to keep.")
def fastqtransform(transform, fastq1, fastq2, fastq3, fastq4, keep_fastq_tags,
                   separate_cb, demuxed_cb, cores, fastq1out, fastq2out,
                   min_length):
    ''' Transform input reads to the tagcounts compatible read layout using
    regular expressions as defined in a transform file. Outputs new format to
    stdout.
    '''
    transform = json.load(open(transform))
    options = _infer_transform_options(transform)
    read_template = '{name}'
    logger.info("Transforming %s." % fastq1)
    if options.dual_index:
        logger.info("Detected dual cellular indexes.")
        if separate_cb:
            read_template += ':CELL_{CB1}-{CB2}'
        else:
            read_template += ':CELL_{CB}'
    elif options.triple_index:
        logger.info("Detected triple cellular indexes.")
        if separate_cb:
            read_template += ':CELL_{CB1}-{CB2}-{CB3}'
        else:
            read_template += ':CELL_{CB}'
    elif options.CB or demuxed_cb:
        logger.info("Detected cellular barcodes.")
        read_template += ':CELL_{CB}'
    if options.MB:
        logger.info("Detected UMI.")
        read_template += ':UMI_{MB}'
    if options.SB:
        logger.info("Detected sample.")
        read_template += ':SAMPLE_{SB}'

    read_template += "{readnum}"

    if keep_fastq_tags:
        read_template += ' {fastqtag}'
    read_template += '\n{seq}\n+\n{qual}\n'

    paired = fastq1out and fastq2out

    read1_regex = re.compile(transform['read1'])
    read2_regex = re.compile(transform['read2']) if fastq2 else None
    read3_regex = re.compile(transform['read3']) if fastq3 else None
    read4_regex = re.compile(transform['read4']) if fastq4 else None

    fastq_file1 = read_fastq(fastq1)
    fastq_file2 = read_fastq(fastq2)
    fastq_file3 = read_fastq(fastq3)
    fastq_file4 = read_fastq(fastq4)

    transform = partial(transformer, read1_regex=read1_regex,
                        read2_regex=read2_regex, read3_regex=read3_regex,
                        read4_regex=read4_regex, paired=paired)

    fastq1out_fh = write_fastq(fastq1out)
    fastq2out_fh = write_fastq(fastq2out)

    p = multiprocessing.Pool(cores)

    try :
        zzip = itertools.izip
    except AttributeError:
        zzip = zip

    chunks = tz.partition_all(10000, zzip(fastq_file1, fastq_file2, fastq_file3,
                                          fastq_file4))
    bigchunks = tz.partition_all(cores, chunks)
    for bigchunk in bigchunks:
        for chunk in p.map(transform, list(bigchunk)):
            if paired:
                for read1_dict, read2_dict in tz.partition(2, chunk):
                    if options.dual_index:
                        if not separate_cb:
                            read1_dict['CB'] = read1_dict['CB1'] + read1_dict['CB2']
                            read2_dict['CB'] = read2_dict['CB1'] + read2_dict['CB2']

                    if demuxed_cb:
                        read1_dict['CB'] = demuxed_cb
                        read2_dict['CB'] = demuxed_cb

                    # Deal with spaces in read names
                    if keep_fastq_tags:
                        name, tag = read1_dict['name'].split(' ')
                        read1_dict['name'] = name
                        read1_dict['fastqtag'] = tag
                        name, tag = read2_dict['name'].split(' ')
                        read2_dict['name'] = name
                        read2_dict['fastqtag'] = tag
                    else:
                        read1_dict['name'] = read1_dict['name'].partition(' ')[0]
                        read2_dict['name'] = read2_dict['name'].partition(' ')[0]
                    read1_dict = _extract_readnum(read1_dict)
                    read2_dict = _extract_readnum(read2_dict)

                    tooshort = (len(read1_dict['seq']) < min_length or
                                len(read2_dict['seq']) < min_length)

                    if not tooshort:
                        fastq1out_fh.write(read_template.format(**read1_dict))
                        fastq2out_fh.write(read_template.format(**read2_dict))
            else:
                for read1_dict in chunk:
                    if options.dual_index:
                        if not separate_cb:
                            read1_dict['CB'] = read1_dict['CB1'] + read1_dict['CB2']

                    if demuxed_cb:
                        read1_dict['CB'] = demuxed_cb

                    # Deal with spaces in read names
                    if keep_fastq_tags:
                        name, tag = read1_dict['name'].split(' ')
                        read1_dict['name'] = name
                        read1_dict['fastqtag'] = tag
                    else:
                        read1_dict['name'] = read1_dict['name'].partition(' ')[0]
                    read1_dict = _extract_readnum(read1_dict)
                    if len(read1_dict['seq']) >= min_length:
                        if fastq1out_fh:
                            fastq1out_fh.write(read_template.format(**read1_dict))
                        else:
                            sys.stdout.write(read_template.format(**read1_dict))

def _is_umi_only(options):
    return options.MB and not options.CB

def _infer_transform_options(transform):
    """
    figure out what transform options should be by examining the provided
    regexes for keywords
    """
    TransformOptions = collections.namedtuple("TransformOptions",
                                              ['CB', 'dual_index', 'triple_index', 'MB', 'SB'])
    CB = False
    SB = False
    MB = False
    dual_index = False
    triple_index = False
    for rx in transform.values():
        if not rx:
            continue
        if "CB1" in rx:
            if "CB3" in rx:
                triple_index = True
            else:
                dual_index = True
        if "SB" in rx:
            SB = True
        if "CB" in rx:
            CB = True
        if "MB" in rx:
            MB = True
    return TransformOptions(CB=CB, dual_index=dual_index, triple_index=triple_index, MB=MB, SB=SB)

def _extract_readnum(read_dict):
    """Extract read numbers from old-style fastqs.

    Handles read 1 and 2 specifications where naming is
    readname/1 readname/2
    """
    pat = re.compile(r"(?P<readnum>/\d+)$")
    parts = pat.split(read_dict["name"])
    if len(parts) == 3:
        name, readnum, endofline = parts
        read_dict["name"] = name
        read_dict["readnum"] = readnum
    else:
        read_dict["readnum"] = ""
    return read_dict

def transformer(chunk, read1_regex, read2_regex, read3_regex, read4_regex,
                paired=False):
    # Parse the reads with the regexes
    update_keys = ("MB", "CB", "CB1", "CB2", "SP")
    reads = []
    for read1, read2, read3, read4 in chunk:
        read1_match = read1_regex.search(read1)
        if not read1_match:
            continue

        read1_dict = read1_match.groupdict()

        if read2_regex:
            read2_match = read2_regex.search(read2)
            if not read2_match:
                continue

            read2_dict = read2_match.groupdict()

        else:
            read2_dict = dict()

        if read3_regex:
            read3_match = read3_regex.search(read3)
            if not read3_match:
                continue

            read3_dict = read3_match.groupdict()

        else:
            read3_dict = dict()

        if read4_regex:
            read4_match = read4_regex.search(read4)
            if not read4_match:
                continue

            read4_dict = read4_match.groupdict()

        else:
            read4_dict = dict()


        if paired:
            read1_dict.update({k: v for k, v in read2_dict.items() if k not
                               in read1_dict})
            read1_dict.update({k: v for k, v in read3_dict.items() if k not
                               in read1_dict})
            read1_dict.update({k: v for k, v in read4_dict.items() if k not
                               in read1_dict})
            read2_dict.update({k: v for k, v in read1_dict.items() if k not
                               in read2_dict})
            read2_dict.update({k: v for k, v in read3_dict.items() if k not
                               in read2_dict})
            read2_dict.update({k: v for k, v in read4_dict.items() if k not
                               in read2_dict})
        else:
            read1_dict.update(read2_dict)
            read1_dict.update(read3_dict)
            read1_dict.update(read4_dict)

        # Output the restrutured read
        reads.append(read1_dict)

        if paired:
            reads.append(read2_dict)

    return reads

@click.command()
@click.argument('sam')
@click.argument('out')
@click.option('--genemap', required=False, default=None,
                help=('A TSV file mapping transcript ids to gene ids. If '
                      'provided expression will be summarised to gene level '
                      '(recommended).'))
@click.option('--output_evidence_table', default=None)
@click.option('--positional', default=False, is_flag=True)
@click.option('--minevidence', required=False, default=1.0, type=float)
@click.option('--cb_histogram', default=None,
                help=('A TSV file with CBs and a count. If the counts are '
                      'are the number of reads at a CB, the cb_cutoff option '
                      'can be used to filter out CBs to be counted.'))
@click.option('--cb_cutoff', default=None,
                help=("Number of counts to filter cellular barcodes. Set to "
                      "'auto' to calculate a cutoff automatically."))
@click.option('--no_scale_evidence', default=False, is_flag=True)
@click.option('--subsample', required=False, default=None, type=int)
@click.option('--sparse', is_flag=True, default=False,
                help="Ouput counts in MatrixMarket format.")
@click.option('--parse_tags', required=False, is_flag=True,
                help=('Parse BAM tags in stead of read name. In this mode '
                      'the optional tags UM and CR will be used for UMI and '
                      'cell barcode, respetively.'))
@click.option('--gene_tags', required=False, is_flag=True,
                help=('Use the optional TX and GX tags in the BAM file to '
                      'read gene mapping information in stead of the mapping '
                      'target nane. Useful if e.g. reads have been mapped to '
                      'genome in stead of transcriptome.'))
def tagcount(sam, out, genemap, output_evidence_table, positional, minevidence,
             cb_histogram, cb_cutoff, no_scale_evidence, subsample, sparse,
             parse_tags, gene_tags):
    ''' Count up evidence for tagged molecules
    '''
    from pysam import AlignmentFile

    from io import StringIO
    import pandas as pd

    from utils import weigh_evidence

    logger.info('Reading optional files')

    gene_map = None
    if genemap:
        with open(genemap) as fh:
            try:
                gene_map = dict(p.strip().split() for p in fh)
            except ValueError:
                logger.error('Incorrectly formatted gene_map, need to be tsv.')
                sys.exit()

    if positional:
        tuple_template = '{0},{1},{2},{3}'
    else:
        tuple_template = '{0},{1},{3}'

    if not cb_cutoff:
        cb_cutoff = 0

    if cb_histogram and cb_cutoff == "auto":
        cb_cutoff = guess_depth_cutoff(cb_histogram)

    cb_cutoff = int(cb_cutoff)

    cb_hist = None
    filter_cb = False
    if cb_histogram:
        cb_hist = pd.read_csv(cb_histogram, index_col=0, header=-1, squeeze=True, sep="\t")
        total_num_cbs = cb_hist.shape[0]
        cb_hist = cb_hist[cb_hist > cb_cutoff]
        logger.info('Keeping {} out of {} cellular barcodes.'.format(cb_hist.shape[0], total_num_cbs))
        filter_cb = True

    parser_re = re.compile('.*:CELL_(?P<CB>.*):UMI_(?P<MB>.*)')

    if subsample:
        logger.info('Creating reservoir of subsampled reads ({} per cell)'.format(subsample))
        start_sampling  = time.time()

        reservoir = collections.defaultdict(list)
        cb_hist_sampled = 0 * cb_hist
        cb_obs = 0 * cb_hist

        track = stream_bamfile(sam)
        current_read = 'none_observed_yet'
        for i, aln in enumerate(track):
            if aln.qname == current_read:
                continue

            current_read = aln.qname

            if parse_tags:
                CB = aln.get_tag('CR')
            else:
                match = parser_re.match(aln.qname)
                CB = match.group('CB')

            if CB not in cb_hist.index:
                continue

            cb_obs[CB] += 1
            if len(reservoir[CB]) < subsample:
                reservoir[CB].append(i)
                cb_hist_sampled[CB] += 1
            else:
                s = pd.np.random.randint(0, cb_obs[CB])
                if s < subsample:
                    reservoir[CB][s] = i

        index_filter = set(itertools.chain.from_iterable(reservoir.values()))
        sam_file.close()
        sampling_time = time.time() - start_sampling
        logger.info('Sampling done - {:.3}s'.format(sampling_time))

    evidence = collections.defaultdict(int)

    logger.info('Tallying evidence')
    start_tally = time.time()

    sam_mode = 'r' if sam.endswith(".sam") else 'rb'
    sam_file = AlignmentFile(sam, mode=sam_mode)
    targets = [x["SN"] for x in sam_file.header["SQ"]]
    track = sam_file.fetch(until_eof=True)
    count = 0
    unmapped = 0
    kept = 0
    nomatchcb = 0
    current_read = 'none_observed_yet'
    count_this_read = True
    missing_transcripts = set()
    for i, aln in enumerate(track):
        if count and not count % 1000000:
            logger.info("Processed %d alignments, kept %d." % (count, kept))
            logger.info("%d were filtered for being unmapped." % unmapped)
            if filter_cb:
                logger.info("%d were filtered for not matching known barcodes."
                            % nomatchcb)
        count += 1

        if aln.is_unmapped:
            unmapped += 1
            continue

        if gene_tags and not aln.has_tag('GX'):
            unmapped += 1
            continue

        if aln.qname != current_read:
            current_read = aln.qname
            if subsample and i not in index_filter:
                count_this_read = False
                continue
            else:
                count_this_read = True
        else:
            if not count_this_read:
                continue

        if parse_tags:
            CB = aln.get_tag('CR')
        else:
            match = parser_re.match(aln.qname)
            CB = match.group('CB')

        if filter_cb:
            if CB not in cb_hist.index:
                nomatchcb += 1
                continue

        if parse_tags:
            MB = aln.get_tag('UM')
        else:
            MB = match.group('MB')

        if gene_tags:
            target_name = aln.get_tag('GX').split(',')[0]
        else:
            txid = sam_file.getrname(aln.reference_id)
            if gene_map:
                if txid in gene_map:
                    target_name = gene_map[txid]
                else:
                    missing_transcripts.add(txid)
                    target_name = txid
            else:
                target_name = txid

        e_tuple = tuple_template.format(CB, target_name, aln.pos, MB)

        # Scale evidence by number of hits
        if no_scale_evidence:
            evidence[e_tuple] += 1.0
        else:
            evidence[e_tuple] += weigh_evidence(aln.tags)

        kept += 1

    tally_time = time.time() - start_tally
    if missing_transcripts:
        logger.warn('The following transcripts were missing gene_ids, so we added them as the transcript ids: %s' % str(missing_transcripts))
    logger.info('Tally done - {:.3}s, {:,} alns/min'.format(tally_time, int(60. * count / tally_time)))
    logger.info('Collapsing evidence')

    logger.info('Writing evidence')
    with tempfile.NamedTemporaryFile('w+t') as out_handle:
        for key in evidence:
            line = '{},{}\n'.format(key, evidence[key])
            out_handle.write(line)

        out_handle.flush()
        out_handle.seek(0)

        evidence_table = pd.read_csv(out_handle, header=None)

    del evidence

    evidence_query = 'evidence >= %f' % minevidence
    if positional:
        evidence_table.columns=['cell', 'gene', 'umi', 'pos', 'evidence']
        collapsed = evidence_table.query(evidence_query).groupby(['cell', 'gene'])['umi', 'pos'].size()

    else:
        evidence_table.columns=['cell', 'gene', 'umi', 'evidence']
        collapsed = evidence_table.query(evidence_query).groupby(['cell', 'gene'])['umi'].size()

    expanded = collapsed.unstack().T

    if gene_map:
        # This Series is just for sorting the index
        genes = pd.Series(index=set(gene_map.values()))
        genes = genes.sort_index()
        # Now genes is assigned to a DataFrame
        genes = expanded.ix[genes.index]

    elif gene_tags:
        expanded.sort_index()
        genes = expanded

    else:
        # make data frame have a complete accounting of transcripts
        targets = pd.Series(index=set(targets))
        targets = targets.sort_index()
        expanded = expanded.reindex(targets.index.values, fill_value=0)
        genes = expanded

    genes.fillna(0, inplace=True)
    genes = genes.astype(int)
    genes.index.name = "gene"

    logger.info('Output results')

    if subsample:
        cb_hist_sampled.to_csv('ss_{}_'.format(subsample) + os.path.basename(cb_histogram), sep='\t')

    if output_evidence_table:
        import shutil
        buf.seek(0)
        with open(output_evidence_table, 'w') as etab_fh:
            shutil.copyfileobj(buf, etab_fh)

    if sparse:
        pd.Series(genes.index).to_csv(out + ".rownames", index=False, header=False)
        pd.Series(genes.columns.values).to_csv(out + ".colnames", index=False, header=False)
        with open(out, "w+b") as out_handle:
            scipy.io.mmwrite(out_handle, scipy.sparse.csr_matrix(genes))
    else:
        genes.to_csv(out)

@click.command()
@click.argument('sam')
@click.argument('out')
@click.option('--genemap', required=False, default=None,
                help=('A TSV file mapping transcript ids to gene ids. If '
                      'provided expression will be summarised to gene level '
                      '(recommended).'))
@click.option('--positional', default=False, is_flag=True)
@click.option('--minevidence', required=False, default=1.0, type=float)
@click.option('--cb_histogram', default=None,
                help=('A TSV file with CBs and a count. If the counts are '
                      'are the number of reads at a CB, the cb_cutoff option '
                      'can be used to filter out CBs to be counted.'))
@click.option('--cb_cutoff', default=None,
                help=("Number of counts to filter cellular barcodes. Set to "
                      "'auto' to calculate a cutoff automatically."))
@click.option('--subsample', required=False, default=None, type=int)
@click.option('--parse_tags', required=False, is_flag=True,
                help=('Parse BAM tags in stead of read name. In this mode '
                      'the optional tags UM and CR will be used for UMI and '
                      'cell barcode, respetively.'))
@click.option('--gene_tags', required=False, is_flag=True,
                help=('Use the optional TX and GX tags in the BAM file to '
                      'read gene mapping information in stead of the mapping '
                      'target nane. Useful if e.g. reads have been mapped to '
                      'genome in stead of transcriptome.'))
@click.option('--umi_matrix', required=False, 
              help=('Save a sparse matrix of counts without UMI deduping to this file.'))
def fasttagcount(sam, out, genemap, positional, minevidence, cb_histogram, 
                 cb_cutoff, subsample, parse_tags, gene_tags, umi_matrix):
    ''' Count up evidence for tagged molecules, this implementation assumes the
    alignment file is coordinate sorted
    '''
    from pysam import AlignmentFile

    from io import StringIO
    import pandas as pd

    from utils import weigh_evidence

    if sam.endswith(".sam"):
        logger.error("To use the fasttagcount subcommand, the alignment file must be a "
                     "coordinate sorted, indexed BAM file.")
        sys.exit(1)

    logger.info('Reading optional files')

    gene_map = None
    if genemap:
        with open(genemap) as fh:
            try:
                gene_map = dict(p.strip().split() for p in fh)
            except ValueError:
                logger.error('Incorrectly formatted gene_map, need to be tsv.')
                sys.exit()

    if positional:
        tuple_template = '{0},{1},{2},{3}'
    else:
        tuple_template = '{0},{1},{3}'

    if not cb_cutoff:
        cb_cutoff = 0

    if cb_histogram and cb_cutoff == "auto":
        cb_cutoff = guess_depth_cutoff(cb_histogram)

    cb_cutoff = int(cb_cutoff)

    cb_hist = None
    filter_cb = False
    if cb_histogram:
        cb_hist = pd.read_csv(cb_histogram, index_col=0, header=-1, squeeze=True, sep="\t")
        total_num_cbs = cb_hist.shape[0]
        cb_hist = cb_hist[cb_hist > cb_cutoff]
        logger.info('Keeping {} out of {} cellular barcodes.'.format(cb_hist.shape[0], total_num_cbs))
        filter_cb = True

    parser_re = re.compile('.*:CELL_(?P<CB>.*):UMI_(?P<MB>.*)')

    if subsample:
        logger.info('Creating reservoir of subsampled reads ({} per cell)'.format(subsample))
        start_sampling  = time.time()

        reservoir = collections.defaultdict(list)
        cb_hist_sampled = 0 * cb_hist
        cb_obs = 0 * cb_hist

        track = stream_bamfile(sam)
        current_read = 'none_observed_yet'
        for i, aln in enumerate(track):
            if aln.qname == current_read:
                continue

            current_read = aln.qname

            if parse_tags:
                CB = aln.get_tag('CR')
            else:
                match = parser_re.match(aln.qname)
                CB = match.group('CB')

            if CB not in cb_hist.index:
                continue

            cb_obs[CB] += 1
            if len(reservoir[CB]) < subsample:
                reservoir[CB].append(i)
                cb_hist_sampled[CB] += 1
            else:
                s = pd.np.random.randint(0, cb_obs[CB])
                if s < subsample:
                    reservoir[CB][s] = i

        index_filter = set(itertools.chain.from_iterable(reservoir.values()))
        sam_file.close()
        sampling_time = time.time() - start_sampling
        logger.info('Sampling done - {:.3}s'.format(sampling_time))

    evidence = collections.defaultdict(lambda: collections.defaultdict(float))
    bare_evidence = collections.defaultdict(float)
    logger.info('Tallying evidence')
    start_tally = time.time()

    sam_mode = 'r' if sam.endswith(".sam") else 'rb'
    sam_file = AlignmentFile(sam, mode=sam_mode)
    transcript_map = collections.defaultdict(set)
    sam_transcripts = [x["SN"] for x in sam_file.header["SQ"]]
    if gene_map:
        for transcript, gene in gene_map.items():
            if transcript in sam_transcripts:
                transcript_map[gene].add(transcript)
    else:
        for transcript in sam_transcripts:
            transcript_map[transcript].add(transcript)
    missing_transcripts = set()
    alignments_processed = 0
    unmapped = 0
    kept = 0
    nomatchcb = 0
    current_read = 'none_observed_yet'
    current_transcript = None
    count_this_read = True
    transcripts_processed = 0
    genes_processed = 0
    cells = list(cb_hist.index)
    targets_seen = set()

    if umi_matrix:
        bare_evidence_handle = open(umi_matrix, "w")
        bare_evidence_handle.write(",".join(["gene"] + cells) + "\n")

    with open(out, "w") as out_handle:
        out_handle.write(",".join(["gene"] + cells) + "\n")
        for gene, transcripts in transcript_map.items():
            for transcript in transcripts:
                for aln in sam_file.fetch(transcript):
                    alignments_processed += 1

                    if aln.is_unmapped:
                        unmapped += 1
                        continue

                    if gene_tags and not aln.has_tag('GX'):
                        unmapped += 1
                        continue

                    if aln.qname != current_read:
                        current_read = aln.qname
                        if subsample and i not in index_filter:
                            count_this_read = False
                            continue
                        else:
                            count_this_read = True
                    else:
                        if not count_this_read:
                            continue

                    if parse_tags:
                        CB = aln.get_tag('CR')
                    else:
                        match = parser_re.match(aln.qname)
                        CB = match.group('CB')

                    if filter_cb:
                        if CB not in cb_hist.index:
                            nomatchcb += 1
                            continue

                    if parse_tags:
                        MB = aln.get_tag('UM')
                    else:
                        MB = match.group('MB')

                    if gene_tags:
                        target_name = aln.get_tag('GX').split(',')[0]
                    else:
                        txid = sam_file.getrname(aln.reference_id)
                        if gene_map:
                            if txid in gene_map:
                                target_name = gene_map[txid]
                            else:
                                missing_transcripts.add(txid)
                                continue
                        else:
                            target_name = txid
                    targets_seen.add(target_name)

                    # Scale evidence by number of hits
                    evidence[CB][MB] += weigh_evidence(aln.tags)
                    bare_evidence[CB] += weigh_evidence(aln.tags)
                    kept += 1
                transcripts_processed += 1
                if not transcripts_processed % 1000:
                    logger.info("%d genes processed." % genes_processed)
                    logger.info("%d transcripts processed." % transcripts_processed)
                    logger.info("%d alignments processed." % alignments_processed)

            earray = []
            for cell in cells:
                umis = [1 for _, v in evidence[cell].items() if v >= minevidence]
                earray.append(str(sum(umis)))
            out_handle.write(",".join([gene] + earray) + "\n")
            earray = []
            if umi_matrix:
                for cell in cells:
                    earray.append(str(int(bare_evidence[cell])))
                bare_evidence_handle.write(",".join([gene] + earray) + "\n")

            evidence = collections.defaultdict(lambda: collections.defaultdict(int))
            bare_evidence = collections.defaultdict(int)
            genes_processed += 1

    if umi_matrix:
        bare_evidence_handle.close()

    # fill dataframe with missing values, sort and output
    df = pd.read_csv(out, index_col=0, header=0)
    targets = pd.Series(index=set(transcript_map.keys()))
    targets = targets.sort_index()
    df = df.reindex(targets.index.values, fill_value=0)
    df = df.sort_index()
    df.to_csv(out)

    if umi_matrix:
        df = pd.read_csv(umi_matrix, index_col=0, header=0)
        df = df.reindex(targets.index.values, fill_value=0)
        df = df.sort_index()
        df.to_csv(umi_matrix)


@click.command()
@click.argument("csv")
@click.argument("sparse")
def sparse(csv, sparse):
    ''' Convert a CSV file to a sparse matrix with rows and column names
    saved as companion files.
    '''
    import pandas as pd
    df = pd.read_csv(csv, index_col=0, header=0)
    pd.Series(df.index).to_csv(sparse + ".rownames", index=False)
    pd.Series(df.columns.values).to_csv(sparse + ".colnames", index=False)
    with open(sparse, "w+b") as out_handle:
        scipy.io.mmwrite(out_handle, scipy.sparse.csr_matrix(df))

@click.command()
@click.argument('fastq', required=True)
@click.option("--umi_histogram", required=False,
               help=("Output a count of each UMI for each cellular barcode to this "
                     "file."))
def cb_histogram(fastq, umi_histogram):
    ''' Counts the number of reads for each cellular barcode

    Expects formatted fastq files.
    '''
    annotations = detect_fastq_annotations(fastq)
    re_string = construct_transformed_regex(annotations)
    parser_re = re.compile(re_string)

    cb_counter = collections.Counter()
    umi_counter = collections.Counter()

    for read in read_fastq(fastq):
        match = parser_re.search(read).groupdict()
        cb = match['CB']
        cb_counter[cb] += 1
        if umi_histogram:
            umi = match['MB']
            umi_counter[(cb, umi)] += 1

    for bc, count in cb_counter.most_common():
        sys.stdout.write('{}\t{}\n'.format(bc, count))

    if umi_histogram:
        with open(umi_histogram, "w") as umi_handle:
            for cbumi, count in umi_counter.most_common():
                umi_handle.write('{}\t{}\t{}\n'.format(cbumi[0], cbumi[1], count))

@click.command()
@click.argument('fastq', required=True)
def umi_histogram(fastq):
    ''' Counts the number of reads for each UMI

    Expects formatted fastq files.
    '''
    annotations = detect_fastq_annotations(fastq)
    re_string = construct_transformed_regex(annotations)
    parser_re = re.compile(re_string)

    counter = collections.Counter()
    for read in read_fastq(fastq):
        match = parser_re.search(read).groupdict()
        counter[match['MB']] += 1

    for bc, count in counter.most_common():
        sys.stdout.write('{}\t{}\n'.format(bc, count))

def get_cb_depth_set(cb_histogram, cb_cutoff):
    ''' Returns a set of barcodes with a minimum number of reads
    '''
    cb_keep_set = set()
    if not cb_histogram:
        return cb_keep_set

    with read_cbhistogram(cb_histogram) as fh:
        cb_map = dict(p.strip().split() for p in fh)
        cb_keep_set = set([k for k, v in cb_map.items() if int(v) > cb_cutoff])
        logger.info('Keeping %d out of %d cellular barcodes.'
                    % (len(cb_keep_set), len(cb_map)))
    return cb_keep_set

def guess_depth_cutoff(cb_histogram):
    ''' Guesses at an appropriate barcode cutoff
    '''
    with read_cbhistogram(cb_histogram) as fh:
        cb_vals = [int(p.strip().split()[1]) for p in fh]
    histo = np.histogram(np.log10(cb_vals), bins=50)
    vals = histo[0]
    edges = histo[1]
    mids = np.array([(edges[i] + edges[i+1])/2 for i in range(edges.size - 1)])
    wdensity = vals * (10**mids) / sum(vals * (10**mids))
    baseline = np.median(wdensity)
    wdensity = list(wdensity)
    # find highest density in upper half of barcode distribution
    peak = wdensity.index(max(wdensity[len(wdensity)/2:]))
    cutoff = None
    for index, dens in reversed(list(enumerate(wdensity[1:peak]))):
        if dens < 2 * baseline:
            cutoff = index
            break
    if not cutoff:
        return None
    else:
        cutoff = 10**mids[cutoff]
        logger.info('Setting barcode cutoff to %d' % cutoff)
        return cutoff

@click.command()
@click.argument('fastq', required=True)
@click.option('--bc1', default=None, required=True)
@click.option('--bc2', default=None)
@click.option('--bc3', default=None)
@click.option('--cores', default=1)
@click.option('--nedit', default=0)
def cb_filter(fastq, bc1, bc2, bc3, cores, nedit):
    ''' Filters reads with non-matching barcodes
    Expects formatted fastq files.
    '''

    with open_gzipsafe(bc1) as bc1_fh:
        bc1 = set(cb.strip() for cb in bc1_fh)
    if bc2:
        with open_gzipsafe(bc2) as bc2_fh:
            bc2 = set(cb.strip() for cb in bc2_fh)
    if bc3:
        with open_gzipsafe(bc3) as bc3_fh:
            bc3 = set(cb.strip() for cb in bc3_fh)

    annotations = detect_fastq_annotations(fastq)
    re_string = construct_transformed_regex(annotations)

    if nedit == 0:
        filter_cb = partial(exact_barcode_filter, bc1=bc1, bc2=bc2, bc3=bc3,
                            re_string=re_string)
    else:
        bc1hash = MutationHash(bc1, nedit)
        bc2hash = None
        bc3hash = None
        if bc2:
            bc2hash = MutationHash(bc2, nedit)
        if bc3:
            bc3hash = MutationHash(bc3, nedit)
        filter_cb = partial(correcting_barcode_filter, bc1hash=bc1hash,
                            bc2hash=bc2hash, bc3hash=bc3hash, re_string=re_string)
    p = multiprocessing.Pool(cores)

    chunks = tz.partition_all(10000, read_fastq(fastq))
    bigchunks = tz.partition_all(cores, chunks)
    for bigchunk in bigchunks:
        for chunk in p.map(filter_cb, list(bigchunk)):
            for read in chunk:
                sys.stdout.write(read)

@click.command()
@click.argument('fastq', required=True)
@click.option('--bc', type=click.File('r'))
@click.option('--cores', default=1)
@click.option('--nedit', default=0)
def sb_filter(fastq, bc, cores, nedit):
    ''' Filters reads with non-matching sample barcodes
    Expects formatted fastq files.
    '''
    barcodes = set(sb.strip() for sb in bc)
    if nedit == 0:
        filter_sb = partial(exact_sample_filter2, barcodes=barcodes)
    else:
        barcodehash = MutationHash(barcodes, nedit)
        filter_sb = partial(correcting_sample_filter2, barcodehash=barcodehash)
    p = multiprocessing.Pool(cores)

    chunks = tz.partition_all(10000, read_fastq(fastq))
    bigchunks = tz.partition_all(cores, chunks)
    for bigchunk in bigchunks:
        for chunk in p.map(filter_sb, list(bigchunk)):
            for read in chunk:
                sys.stdout.write(read)

@click.command()
@click.argument('fastq', required=True)
@click.option('--cores', default=1)
def mb_filter(fastq, cores):
    ''' Filters umis with non-ACGT bases
    Expects formatted fastq files.
    '''
    filter_mb = partial(umi_filter)
    p = multiprocessing.Pool(cores)

    chunks = tz.partition_all(10000, read_fastq(fastq))
    bigchunks = tz.partition_all(cores, chunks)
    for bigchunk in bigchunks:
        for chunk in p.map(filter_mb, list(bigchunk)):
            for read in chunk:
                sys.stdout.write(read)

@click.command()
@click.argument('fastq', required=True)
@click.option('--cores', default=1)
def add_uid(fastq, cores):
    ''' Adds UID:[samplebc cellbc umi] to readname for umi-tools deduplication
    Expects formatted fastq files with correct sample and cell barcodes.
    '''

    uids = partial(append_uids)
    p = multiprocessing.Pool(cores)

    chunks = tz.partition_all(10000, read_fastq(fastq))
    bigchunks = tz.partition_all(cores, chunks)
    for bigchunk in bigchunks:
        for chunk in p.map(uids, list(bigchunk)):
            for read in chunk:
                sys.stdout.write(read)

def write_kallisto_chunk(out_dir, cb, chunk):
    fq_fn = os.path.join(out_dir, cb + ".fq")
    umi_fn = os.path.join(out_dir, cb + ".umi")
    with open(fq_fn, "a") as fq_handle, open(umi_fn, "a") as umi_handle:
        for read, umi in chunk:
            fq_handle.write(read)
            umi_handle.write(umi + "\n")

@click.command()
@click.argument('fastq', required=True)
@click.option('--out_dir', default=".")
@click.option('--cb_histogram', default=None)
@click.option('--cb_cutoff', default=0)
def kallisto(fastq, out_dir, cb_histogram, cb_cutoff):
    ''' Convert fastqtransformed file to output format compatible with
    kallisto.
    '''
    parser_re = re.compile('(.*):CELL_(?<CB>.*):UMI_(?P<UMI>.*)\\n(.*)\\n\\+\\n(.*)\\n')
    if fastq.endswith('gz'):
        fastq_fh = gzip.GzipFile(fileobj=open(fastq))
    elif fastq == "-":
        fastq_fh = sys.stdin
    else:
        fastq_fh = open(fastq)

    cb_depth_set = get_cb_depth_set(cb_histogram, cb_cutoff)

    cb_set = set()
    cb_batch = collections.defaultdict(list)
    parsed = 0
    for read in stream_fastq(fastq_fh):
        match = parser_re.search(read).groupdict()
        umi = match['UMI']
        cb = match['CB']
        if cb_depth_set and cb not in cb_depth_set:
            continue
        parsed += 1
        cb_set.add(cb)
        cb_batch[cb].append((read, umi))
        # write in batches to avoid opening up file handles repeatedly
        if not parsed % 10000000:
            for cb, chunk in cb_batch.items():
                write_kallisto_chunk(out_dir, cb, chunk)
            cb_batch = collections.defaultdict(list)

    for cb, chunk in cb_batch.items():
        write_kallisto_chunk(out_dir, cb, chunk)

    with open(os.path.join(out_dir, "barcodes.batch"), "w") as out_handle:
        out_handle.write("#id umi-file file-1\n")
        batchformat = "{cb} {cb}.umi {cb}.fq\n"
        for cb in cb_set:
            out_handle.write(batchformat.format(**locals()))


@click.command()
@click.argument('sam', required=True)
def bamtag(sam):
    ''' Convert a BAM/SAM with fastqtransformed read names to have UMI and
    cellular barcode tags
    '''
    from pysam import AlignmentFile

    start_time = time.time()

    sam_file = open_bamfile(sam)
    out_file = AlignmentFile("-", "wh", template=sam_file)
    track = sam_file.fetch(until_eof=True)

    # peek at first alignment to determine the annotations
    if is_python3():
        queryalignment = next(track)
    else:
        queryalignment = track.next()
    annotations = detect_alignment_annotations(queryalignment)
    track = itertools.chain([queryalignment], track)

    re_string = construct_transformed_regex(annotations)
    parser_re = re.compile(re_string)

    for count, aln in enumerate(track, start=1):
        if count and not count % 1000000:
            logger.info("Processed %d alignments." % count)

        match = parser_re.match(aln.qname)
        tags = aln.tags

        if "cellular" in annotations:
            aln.tags += [('XC', match.group('CB'))]
        if "molecular" in annotations:
            aln.tags += [('RX', match.group('MB'))]
        if "sample" in annotations:
            aln.tags += [('XS', match.group('SB'))]

        out_file.write(aln)

    total_time = time.time() - start_time
    logger.info('BAM tag conversion done - {:.3}s, {:,} alns/min'.format(total_time, int(60. * count / total_time)))
    logger.info("Processed %d alignments." % count)

@click.command()
@click.argument('fastq', required=True)
@click.option('--out_dir', default=".")
@click.option('--nedit', default=0)
@click.option('--barcodes', type=click.File('r'), required=False)
def demultiplex_samples(fastq, out_dir, nedit, barcodes):
    ''' Demultiplex a fastqtransformed FASTQ file into a FASTQ file for
    each sample.
    '''
    annotations = detect_fastq_annotations(fastq)
    re_string = construct_transformed_regex(annotations)
    parser_re = re.compile(re_string)

    if barcodes:
        barcodes = set(barcode.strip() for barcode in barcodes)
    else:
        barcodes = set()

    if nedit == 0:
        filter_bc = partial(exact_sample_filter, barcodes=barcodes)
    else:
        barcodehash = MutationHash(barcodes, nedit)
        filter_bc = partial(correcting_sample_filter, barcodehash=barcodehash)

    sample_set = set()
    batch = collections.defaultdict(list)
    parsed = 0
    safe_makedir(out_dir)
    for read in read_fastq(fastq):
        parsed += 1
        read = filter_bc(read)
        if not read:
            continue
        match = parser_re.search(read).groupdict()
        sample = match['SB']
        sample_set.add(sample)
        batch[sample].append(read)
        # write in batches to avoid opening up file handles repeatedly
        if not parsed % 10000000:
            for sample, reads in batch.items():
                out_file = os.path.join(out_dir, sample + ".fq")
                with open(out_file, "a") as out_handle:
                    for read in reads:
                        fixed = filter_bc(read)
                        if fixed:
                            out_handle.write(fixed)
            batch = collections.defaultdict(list)

    for sample, reads in batch.items():
        out_file = os.path.join(out_dir, sample + ".fq")
        with open(out_file, "a") as out_handle:
            for read in reads:
                fixed = filter_bc(read)
                if fixed:
                    out_handle.write(read)

def is_python3():
    return sys.version_info >= (3, 0)

@click.command()
@click.argument('fastq', required=True)
@click.option('--out_dir', default=".")
@click.option('--readnumber', default="")
@click.option('--prefix', default="")
@click.option('--cb_histogram', default=None)
@click.option('--cb_cutoff', default=0)
def demultiplex_cells(fastq, out_dir, readnumber, prefix, cb_histogram, 
                      cb_cutoff):
    ''' Demultiplex a fastqtransformed FASTQ file into a FASTQ file for
    each cell.
    '''
    annotations = detect_fastq_annotations(fastq)
    re_string = construct_transformed_regex(annotations)
    parser_re = re.compile(re_string)
    readstring = "" if not readnumber else "_R{}".format(readnumber)
    filestring = "{prefix}{sample}{readstring}.fq"
    cb_set = set()
    if cb_histogram:
        cb_set = get_cb_depth_set(cb_histogram, cb_cutoff)
    sample_set = set()
    batch = collections.defaultdict(list)
    parsed = 0
    safe_makedir(out_dir)
    for read in read_fastq(fastq):
        parsed += 1
        match = parser_re.search(read).groupdict()
        sample = match['CB']
        if cb_set and sample not in cb_set:
            continue
        sample_set.add(sample)
        batch[sample].append(read)
        # write in batches to avoid opening up file handles repeatedly
        if not parsed % 10000000:
            for sample, reads in batch.items():
                out_file = os.path.join(out_dir, filestring.format(**locals()))
                with open(out_file, "a") as out_handle:
                    for read in reads:
                        out_handle.write(read)
            batch = collections.defaultdict(list)

    for sample, reads in batch.items():
        out_file = os.path.join(out_dir, filestring.format(**locals()))
        with open(out_file, "a") as out_handle:
            for read in reads:
                out_handle.write(read)

@click.command()
@click.argument('SAM', required=True)
@click.argument('barcodes', type=click.File('r'), required=True)
def subset_bamfile(sam, barcodes):
    """
    Subset a SAM/BAM file, keeping only alignments from given
    cellular barcodes
    """
    from pysam import AlignmentFile

    start_time = time.time()

    sam_file = open_bamfile(sam)
    out_file = AlignmentFile("-", "wh", template=sam_file)
    track = sam_file.fetch(until_eof=True)

    # peek at first alignment to determine the annotations
    queryalignment = track.next()
    annotations = detect_alignment_annotations(queryalignment)
    track = itertools.chain([queryalignment], track)

    re_string = construct_transformed_regex(annotations)
    parser_re = re.compile(re_string)
    barcodes = set(barcode.strip() for barcode in barcodes)

    for count, aln in enumerate(track, start=1):
        if count and not count % 1000000:
            logger.info("Processed %d alignments." % count)

        match = parser_re.match(aln.qname)
        tags = aln.tags

        if "cellular" in annotations:
            cb = match.group('CB')
            if cb in barcodes:
                out_file.write(aln)

@click.command()
def version():
    print(VERSION)

@click.group()
def umis():
    pass

umis.add_command(version)
umis.add_command(sparse)
umis.add_command(fastqtransform)
umis.add_command(tagcount)
umis.add_command(fasttagcount)
umis.add_command(cb_histogram, name="cb_histogram")
umis.add_command(umi_histogram, name="umi_histogram")
umis.add_command(cb_filter, name="cb_filter")
umis.add_command(sb_filter, name="sb_filter")
umis.add_command(mb_filter, name="mb_filter")
umis.add_command(add_uid, name="add_uid")
umis.add_command(kallisto)
umis.add_command(bamtag)
umis.add_command(demultiplex_samples, name="demultiplex_samples")
umis.add_command(demultiplex_cells, name="demultiplex_cells")
umis.add_command(subset_bamfile, name="subset_bamfile")
