from difflib import SequenceMatcher
import pandas as pd

dict1 = {0: 'A human orthogonal IL-2 and IL-2R system enhances\nCAR T cell expansion and antitumor activity in a\nmurine model of leukemia (https://www.notion.so/A-human-orthogonal-IL-2-and-IL-2R-system-enhances-CAR-T-cell-expansion-and-antitumor-activity-in-a-m-c9d7658fe6744a7c94596e5d7359d325?pvs=21)',
        1: 'Engineered nasal cartilage forthe repair\nof osteoarthritic knee cartilage defects (https://www.notion.so/Engineered-nasal-cartilage-forthe-repair-of-osteoarthritic-knee-cartilage-defects-c6d0f802247a4dcda340eabca7fdda7e?pvs=21)',
        10: '',
        11: 'Macrophage-tumor chimeric exosomes accumulate\nin lymph node and tumor to activate the immune\nresponse and the tumor microenvironment (https://www.notion.so/Macrophage-tumor-chimeric-exosomes-accumulate-in-lymph-node-and-tumor-to-activate-the-immune-respons-644f3cbbb3e4476abd5b7fceeb72b421?pvs=21)',
        12: 'Genome-encoded cytoplasmic double-stranded RNAs,\nfound in C9ORF72 ALS-FTD brain, propagate\nneuronal loss (https://www.notion.so/Genome-encoded-cytoplasmic-double-stranded-RNAs-found-in-C9ORF72-ALS-FTD-brain-propagate-neuronal--39d4e7e5930049df98522c9eace2990a?pvs=21)',
        13: 'Multicellular modeling of ciliopathy by combining iPS\ncells and microfluidic airway-on-a-chip technology (https://www.notion.so/Multicellular-modeling-of-ciliopathy-by-combining-iPS-cells-and-microfluidic-airway-on-a-chip-techno-666b4719b5674ae8b0128de947d39c03?pvs=21)',
        14: 'Treatment with ROS detoxifying gold quantum clusters\nalleviates the functional decline in a mouse model\nof Friedreich ataxia (https://www.notion.so/Treatment-with-ROS-detoxifying-gold-quantum-clusters-alleviates-the-functional-decline-in-a-mouse-mo-d71410b7f6dd4e349a73ed2412fb72b8?pvs=21)',
        15: 'Repeated Plasmodium falciparum infection in humans drives the clonal expansion of an adaptive ## T cell repertoire (https://www.notion.so/Repeated-Plasmodium-falciparum-infection-in-humans-drives-the-clonal-expansion-of-an-adaptive-T-c-d83de6223481443f86f79bf2aed61b90?pvs=21)',
        16: 'Toward predicting CYP2D6-mediated variable drug\nresponse from CYP2D6 gene sequencing data (https://www.notion.so/Toward-predicting-CYP2D6-mediated-variable-drug-response-from-CYP2D6-gene-sequencing-data-ca196ac9b49142928373e37a4ddab8e3?pvs=21)',
        17: '',
        18: '',
        19: 'Alloantigen-specific type 1 regulatory T cells suppress through CTLA-4 and PD-1 pathways and persist long-term in patients.pdf (https://www.notion.so/Alloantigen-specific-type-1-regulatory-T-cells-suppress-through-CTLA-4-and-PD-1-pathways-and-persist-3d85238ee91145c6b6bdfffa6fc5ddf0?pvs=21)',
        2: 'Selective targeting ofNaV1.7 via inhibition\nofthe CRMP2-Ubc9 interaction reduces\npain in rodents (https://www.notion.so/Selective-targeting-ofNaV1-7-via-inhibition-ofthe-CRMP2-Ubc9-interaction-reduces-pain-in-rodents-69038e682b39494885656616ae3d5e4f?pvs=21)',
        20: '',
        21: 'Lithium preserves peritoneal membrane integrity by suppressing mesothelial cell\n#B-crystallin (https://www.notion.so/Lithium-preserves-peritoneal-membrane-integrity-by-suppressing-mesothelial-cell-B-crystallin-5229d80ea1944c22b1f726078486079b?pvs=21)',
        22: 'Functional impairment of CD19+\nCD24hiCD38hi B cells\nin neuromyelitis optica spectrum disorder is restored by\nB cell depletion therapy (https://www.notion.so/Functional-impairment-of-CD19-CD24hiCD38hi-B-cells-in-neuromyelitis-optica-spectrum-disorder-is-res-8040678f422344ddbd28786a00e91932?pvs=21)',
        23: 'Blockade ofthe CD93 pathway normalizes tumor\nvasculature to facilitate drug delivery\nand immunotherapy (https://www.notion.so/Blockade-ofthe-CD93-pathway-normalizes-tumor-vasculature-to-facilitate-drug-delivery-and-immunothera-64dc2d1f436b4b7dbcdb076440cf5fdb?pvs=21)',
        24: 'Epicardial differentiation drives fibro-fatty remodeling\nin arrhythmogenic cardiomyopathy (https://www.notion.so/Epicardial-differentiation-drives-fibro-fatty-remodeling-in-arrhythmogenic-cardiomyopathy-46bc17ada96a433bb652a16e4e0bcaea?pvs=21)',
        25: 'Therapeutic inhibition of RBM20 improves diastolic\nfunction in a murine heart failure model and human\nengineered heart tissue (https://www.notion.so/Therapeutic-inhibition-of-RBM20-improves-diastolic-function-in-a-murine-heart-failure-model-and-huma-b2b2f01dd8694bbca9c892223894110f?pvs=21)',
        26: 'The MK2/Hsp27 axis is a major survival mechanism for pancreatic ductal\nadenocarcinoma under genotoxic stress (https://www.notion.so/The-MK2-Hsp27-axis-is-a-major-survival-mechanism-for-pancreatic-ductal-adenocarcinoma-under-genotoxi-6ef3b306c3f747e28bfd51894e19d6be?pvs=21)',
        27: 'AD-linked R47H-TREM2 mutation induces disease-enhancing microglial states via AKT hyperactivation (https://www.notion.so/AD-linked-R47H-TREM2-mutation-induces-disease-enhancing-microglial-states-via-AKT-hyperactivation-ddbe2f5f54c345ff9fd22bc5cf456e52?pvs=21)',
        28: 'Neuropeptide S receptor 1 is a nonhormonal\ntreatment target in endometriosis (https://www.notion.so/Neuropeptide-S-receptor-1-is-a-nonhormonal-treatment-target-in-endometriosis-d8d5d21e2b8c40588a0e3df12e21c694?pvs=21)',
        29: 'Chromosomal instability sensitizes patient breast\ntumors to multipolar divisions induced by paclitaxel (https://www.notion.so/Chromosomal-instability-sensitizes-patient-breast-tumors-to-multipolar-divisions-induced-by-paclitax-2ec51c143076439283177ef3ce27ec03?pvs=21)',
        3: 'Truncated titin proteins in dilated cardiomyopathy (https://www.notion.so/Truncated-titin-proteins-in-dilated-cardiomyopathy-954ade321ab6461e95de8f5f6562d0d8?pvs=21)',
        30: 'Targeting multiple cell death pathways extends\nthe shelf life and preserves the function of human\nand mouse neutrophils fortransfusion (https://www.notion.so/Targeting-multiple-cell-death-pathways-extends-the-shelf-life-and-preserves-the-function-of-human-an-34369a6831b4487a92f73802979b958b?pvs=21)',
        31: '',
        32: 'Single-cell profiling of human bone marrow progenitors\nreveals mechanisms of failing erythropoiesis\ninDiamond-Blackfan anemia (https://www.notion.so/Single-cell-profiling-of-human-bone-marrow-progenitors-reveals-mechanisms-of-failing-erythropoiesis--0797ff4d9ad8410980042408789617ca?pvs=21)',
        33: 'Dynamic loading of human engineered heart tissue enhances contractile function and drives a desmosome-linked disease phenotype (https://www.notion.so/Dynamic-loading-of-human-engineered-heart-tissue-enhances-contractile-function-and-drives-a-desmosom-9db92f2d4ca24042aa7fff9730b5b33f?pvs=21)',
        34: 'ALT neuroblastoma chemoresistance due to telomere\ndysfunction–induced ATM activation is reversible\nwith ATM inhibitor AZD0156 (https://www.notion.so/ALT-neuroblastoma-chemoresistance-due-to-telomere-dysfunction-induced-ATM-activation-is-reversible-w-70405903469d4ccba05dddfac17f5a37?pvs=21)',
        35: 'A recombinant commensal bacteria elicits\nheterologous antigen-specific immune responses\nduring pharyngeal carriage (https://www.notion.so/A-recombinant-commensal-bacteria-elicits-heterologous-antigen-specific-immune-responses-during-phary-eae132cb3e164eb9abf88fa36607fc38?pvs=21)',
        36: 'Hippocampal cAMP regulates HCN channel function\non two time scales with differential effects on\nanimal behavior (https://www.notion.so/Hippocampal-cAMP-regulates-HCN-channel-function-on-two-time-scales-with-differential-effects-on-anim-29917aa8926e4f1586f6f9169495d4c1?pvs=21)',
        37: 'Truncated titin proteins and titin haploinsufficiency are\ntargets forfunctional recovery in human\ncardiomyopathy due to TTN mutations (https://www.notion.so/Truncated-titin-proteins-and-titin-haploinsufficiency-are-targets-forfunctional-recovery-in-human-ca-d85431c37e614e0eb595a6c004af6268?pvs=21)',
        38: 'Local delivery of mRNA-encoded cytokines promotes\nantitumor immunity and tumor eradication across\nmultiple preclinical tumor models (https://www.notion.so/Local-delivery-of-mRNA-encoded-cytokines-promotes-antitumor-immunity-and-tumor-eradication-across-mu-e7cc2756db7c47f089d893c331b26d36?pvs=21)',
        4: 'Macrophage migration inhibitory factor drives\npathology in a mouse model of spondyloarthritis and\nis associated with human disease (https://www.notion.so/Macrophage-migration-inhibitory-factor-drives-pathology-in-a-mouse-model-of-spondyloarthritis-and-is-396914560a9f45eaa9a243311f5ed462?pvs=21)',
        5: 'A small-molecule activator of the unfolded protein response eradicates human breast tumors in mice (https://www.notion.so/A-small-molecule-activator-of-the-unfolded-protein-response-eradicates-human-breast-tumors-in-mice-4552e9220c944095858c2519ef9ecd70?pvs=21)',
        6: 'Deleting DNMT3A in CAR T cells prevents exhaustion\nand enhances antitumor activity (https://www.notion.so/Deleting-DNMT3A-in-CAR-T-cells-prevents-exhaustion-and-enhances-antitumor-activity-9faa6e96740845e1b0c5b4116b6e1e83?pvs=21)',
        7: 'Epigenetically defined therapeutic targeting in H3.3G34RV high-grade gliomas.pdf (https://www.notion.so/Epigenetically-defined-therapeutic-targeting-in-H3-3G34RV-high-grade-gliomas-pdf-7338f00b200346a6a18cbc18d0f46dcd?pvs=21)',
        8: 'Targeting AKR1B1 inhibits glutathione de novo\nsynthesis to overcome acquired resistance to\nEGFR-targeted therapy in lung cancer (https://www.notion.so/Targeting-AKR1B1-inhibits-glutathione-de-novo-synthesis-to-overcome-acquired-resistance-to-EGFR-targ-7eca61b3487449349ca7b41da8be9b79?pvs=21)',
        9: 'Mitochondrial–cell cycle cross-talk drives endoreplication in heart disease (https://www.notion.so/Mitochondrial-cell-cycle-cross-talk-drives-endoreplication-in-heart-disease-3cb211bbdc1c4c778778a10d0d922cec?pvs=21)',
       }
dict2 = {y: x for x, y in dict1.items()}

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def remove_spaces(l):
    ul = []
    for i in l:
        if i != '':
            ul.append(i)
    return ul

def convert_string_to_df(s):
    rows = s.split('\n')
    updated_df = []
    for row in rows:
        updated_df.append(remove_spaces(row.strip().split("  ")))
    df = pd.DataFrame(updated_df[1:], columns = ['Index'] + updated_df[0]).drop('Index', axis = 1)
    return df

