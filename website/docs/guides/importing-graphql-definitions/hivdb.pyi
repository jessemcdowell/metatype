from typegraph import t

class TypeList:
    AAReads: t.typedef = ...
    ASIAlgorithm: t.typedef = ...
    AlgorithmComparison: t.typedef = ...
    AlignedGeneSequence: t.typedef = ...
    BoundMutationComment: t.typedef = ...
    BoundMutationPrevalence: t.typedef = ...
    BoundSubtype: t.typedef = ...
    CommentType: t.typedef = ...
    CommentsByType: t.typedef = ...
    ComparableDrugScore: t.typedef = ...
    CustomASIAlgorithm: t.typedef = ...
    CutoffKeyPoint: t.typedef = ...
    DescriptiveStatistics: t.typedef = ...
    Drug: t.typedef = ...
    DrugClass: t.typedef = ...
    DrugClassEnum: t.typedef = ...
    DrugEnum: t.typedef = ...
    DrugPartialScore: t.typedef = ...
    DrugResistance: t.typedef = ...
    DrugResistanceAlgorithm: t.typedef = ...
    DrugScore: t.typedef = ...
    EnumGene: t.typedef = ...
    EnumSequenceReadsHistogramAggregatesOption: t.typedef = ...
    FrameShift: t.typedef = ...
    Gene: t.typedef = ...
    GeneMutations: t.typedef = ...
    GeneSequenceReads: t.typedef = ...
    HIVBoundSubtype: t.typedef = ...
    HIVClassificationLevel: t.typedef = ...
    HIVSubtype: t.typedef = ...
    Mutation: t.typedef = ...
    MutationPrevalence: t.typedef = ...
    MutationPrevalenceByAA: t.typedef = ...
    MutationPrevalenceSubtype: t.typedef = ...
    MutationPrevalenceSubtypeStat: t.typedef = ...
    MutationSetFilterOption: t.typedef = ...
    MutationType: t.typedef = ...
    MutationsAnalysis: t.typedef = ...
    MutationsByType: t.typedef = ...
    OneCodonReads: t.typedef = ...
    OneCodonReadsCoverage: t.typedef = ...
    OneCodonReadsInput: t.typedef = ...
    PositionCodonReads: t.typedef = ...
    PositionCodonReadsInput: t.typedef = ...
    PrettyPairwise: t.typedef = ...
    SIR: t.typedef = ...
    SequenceAnalysis: t.typedef = ...
    SequenceReadsAnalysis: t.typedef = ...
    SequenceReadsHistogram: t.typedef = ...
    SequenceReadsHistogramBin: t.typedef = ...
    SequenceReadsHistogramByCodonReads: t.typedef = ...
    SequenceReadsHistogramByCodonReadsBin: t.typedef = ...
    SequenceReadsInput: t.typedef = ...
    SierraVersion: t.typedef = ...
    Strain: t.typedef = ...
    StrainEnum: t.typedef = ...
    Subtype: t.typedef = ...
    UnalignedSequenceInput: t.typedef = ...
    UnalignedSequenceOutput: t.typedef = ...
    UnsequencedRegion: t.typedef = ...
    UnsequencedRegions: t.typedef = ...
    UntranslatedRegionInput: t.typedef = ...
    ValidationLevel: t.typedef = ...
    ValidationResult: t.typedef = ...
    Viewer: t.typedef = ...

class FuncList:
    currentVersion: t.func = ...
    currentProgramVersion: t.func = ...
    sequenceAnalysis: t.func = ...
    sequenceReadsAnalysis: t.func = ...
    mutationsAnalysis: t.func = ...
    patternAnalysis: t.func = ...
    genes: t.func = ...
    mutationPrevalenceSubtypes: t.func = ...
    viewer: t.func = ...

class Import:
    types: TypeList = ...
    functions: FuncList = ...

def import_hivdb() -> Import: ...
