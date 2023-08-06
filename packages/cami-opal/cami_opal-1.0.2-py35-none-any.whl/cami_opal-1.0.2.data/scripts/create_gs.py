#!python

from collections import defaultdict
from collections import OrderedDict

RANKS = ['superkingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species', 'strain']
DICT_RANK_TO_INDEX = dict(zip(RANKS, list(range(len(RANKS)))))


def load_names(tax_id_to_rank, names_file_path):
    tax_id_to_name = {}
    with open(names_file_path) as read_handler:
        for line in read_handler:
            if len(line.strip()) == 0:
                continue
            line = line.split('|')
            line = list(map(str.strip, line))
            tax_id = line[0]

            if line[3] == "scientific name":
                tax_id_to_name[tax_id] = line[1]
            else:
                continue

            if tax_id_to_rank[tax_id] == "species" or tax_id_to_rank[tax_id] == "strain":
                names = tax_id_to_name[tax_id].split(" ")
                if len(names) > 2:
                    if tax_id_to_rank[tax_id] == "strain":
                        tax_id_to_name[tax_id] = "{} {} strain".format(names[0], names[1])
                    else:
                        tax_id_to_name[tax_id] = "{} {}".format(names[0], names[1])
    tax_id_to_name[""] = ""
    return tax_id_to_name


def set_strain_rank_for_tax_id(tax_id, tax_id_to_parent, tax_id_to_rank):
    if tax_id_to_rank[tax_id] == "no rank" and tax_id_to_parent[tax_id] in tax_id_to_parent and (
            tax_id_to_rank[tax_id_to_parent[tax_id]] == "species" or
            tax_id_to_rank[tax_id_to_parent[tax_id]] == "subspecies" or
            tax_id_to_rank[tax_id_to_parent[tax_id]] == "strain") or tax_id_to_rank[tax_id] == "subspecies":
        tax_id_to_rank[tax_id] = "strain"
        return True
    return False


def load_tax_info(ncbi_nodes_file):
    tax_id_to_parent = {}
    tax_id_to_rank = {}
    with open(ncbi_nodes_file) as read_handler:
        for line in read_handler:
            if len(line.strip()) == 0:
                continue
            line = line.split('|')
            line = list(map(str.strip, line))
            tax_id = line[0]
            tax_id_to_parent[tax_id] = line[1]
            tax_id_to_rank[tax_id] = line[2]

    for tax_id, rank in tax_id_to_rank.items():
        if not set_strain_rank_for_tax_id(tax_id, tax_id_to_parent, tax_id_to_rank):
            if tax_id_to_parent[tax_id] in tax_id_to_parent:
                set_strain_rank_for_tax_id(tax_id_to_parent[tax_id], tax_id_to_parent, tax_id_to_rank)

    return tax_id_to_parent, tax_id_to_rank


def get_id_path(tax_id, tax_id_to_parent, tax_id_to_rank):
    index = DICT_RANK_TO_INDEX[tax_id_to_rank[tax_id]]
    path = [''] * (index + 1)
    path[index] = tax_id

    id = tax_id
    while id in tax_id_to_parent:
        id = tax_id_to_parent[id]
        if id == '1':
            break
        if tax_id_to_rank[id] not in RANKS:
            continue
        index = DICT_RANK_TO_INDEX[tax_id_to_rank[id]]
        if path[index] == '':
            path[index] = id
        if tax_id_to_rank[id] == "superkingdom":
            break
    return path


def main():
    xx = defaultdict()
    try:
        print(xx['a'])
    except KeyError:
        print("no key")
    exit()



    ncbi_nodes_file = "/home/fmeyer/cami/taxonomy/nodes.dmp"
    ncbi_names_file = "/home/fmeyer/cami/taxonomy/names.dmp"

    tax_id_to_parent, tax_id_to_rank = load_tax_info(ncbi_nodes_file)
    tax_id_to_name = load_names(tax_id_to_rank, ncbi_names_file)

    rank_to_tax_id_to_abundance = defaultdict(dict)
    rank_to_tax_id_to_id_path = defaultdict(dict)

    tax_id_list = []
    with open("/home/fmeyer/Opal/submission2/hmp_gs.tsv") as f_read:
        for line in f_read:
            if len(line.strip()) == 0:
                continue
            tax_id, abundance = line.rstrip('\n').split('\t', 1)
            rank = tax_id_to_rank[tax_id]
            try:
                rank_index = DICT_RANK_TO_INDEX[rank]
            except:
                print("{} {}".format(tax_id, rank))
                exit(1)

            rank_to_tax_id_to_abundance[rank_index][tax_id] = float(abundance) * 100
            tax_id_list.append(tax_id)
            # print("{}\t{}\t{}\t{}".format(taxid, tax_id_to_parent[taxid], abundance, tax_id_to_name[taxid]))
            # print(get_id_path(taxid, tax_id_to_parent, tax_id_to_rank))

    strain_index = DICT_RANK_TO_INDEX["strain"]
    for tax_id in tax_id_list:
        rank_to_tax_id_to_id_path[strain_index][tax_id] = get_id_path(tax_id, tax_id_to_parent, tax_id_to_rank)

    for rank in RANKS[:-1]:
        rank_index = DICT_RANK_TO_INDEX[rank]
        # sort rank_to_tax_id_to_id_path such that tax ids. with the same parent become adjacent
        tax_id_to_id_path_sorted = OrderedDict(sorted(rank_to_tax_id_to_id_path[strain_index].items(), key=lambda t: rank_to_tax_id_to_id_path[strain_index][t[0]][rank_index]))
        tax_id2 = None
        for tax_id in tax_id_to_id_path_sorted:
            tax_id_r = tax_id_to_id_path_sorted[tax_id][rank_index]
            if tax_id_r == '':
                tax_id2 = None
                continue
            if tax_id_r == tax_id2:
                rank_to_tax_id_to_abundance[rank_index][tax_id_r] += rank_to_tax_id_to_abundance[strain_index][tax_id]
            else:
                rank_to_tax_id_to_abundance[rank_index][tax_id_r] = rank_to_tax_id_to_abundance[strain_index][tax_id]
                rank_to_tax_id_to_id_path[rank_index][tax_id_r] = rank_to_tax_id_to_id_path[strain_index][tax_id][:rank_index + 1]
            tax_id2 = tax_id_r

    sample_id = "sampleid"

    print("@SampleID:{}\n@Version:0.9.1\n@Ranks:superkingdom|phylum|class|order|family|genus|species|strain\n\n@@TAXID\tRANK\tTAXPATH\tTAXPATHSN\tPERCENTAGE".format(sample_id))
    for rank in RANKS:
        rank_index = DICT_RANK_TO_INDEX[rank]
        for tax_id in rank_to_tax_id_to_abundance[rank_index]:
            id_path = rank_to_tax_id_to_id_path[rank_index][tax_id]
            name_path = []
            for id in id_path:
                name_path.append(tax_id_to_name[id])
            print("{}\t{}\t{}\t{}\t{}".format(tax_id, tax_id_to_rank[tax_id], "|".join(id_path), "|".join(name_path), rank_to_tax_id_to_abundance[rank_index][tax_id]))


main()
