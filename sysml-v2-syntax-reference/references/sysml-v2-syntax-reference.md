# SysML v2.0 Textual Syntax Reference (extracted)

**Source:** OMG SysML v2.0 Part 1: Language Specification (formal/2025-09-03, September 2025), Section 8.2 Concrete Syntax.  
**Purpose:** Single reference for all textual syntax (EBNF and lexical) for tooling, MCP, and editors.  
**Full spec:** [OMG SysML 2.0 Language](https://www.omg.org/spec/SysML/2.0/Language/).

---

## 1. EBNF conventions

### Table 27 – EBNF notation

| Notation | Meaning |
|----------|--------|
| `LEXICAL` | Lexical element |
| `'terminal'` | Terminal element |
| `NonterminalElement` | Non-terminal element |
| `Element1 Element2` | Sequential elements |
| `Element1 \| Element2` | Alternative elements |
| `Element ?` | Optional (zero or one) |
| `Element *` | Repeated (zero or more) |
| `Element +` | Repeated (one or more) |
| `( Elements ... )` | Grouping |

### Table 28 – Abstract syntax synthesis

| Notation | Meaning |
|----------|--------|
| `p = Element` | Assign result of parsing Element to property p |
| `p += Element` | Add result to list property p |
| `p ?= Element` | If Element is parsed, set Boolean property p to true |
| `{ p = value }` / `{ p += value }` | Assign/add value without parsing; "this" = element being synthesized |
| `[QualifiedName]` | Parse QualifiedName, resolve to Element reference for use as value |

### Table 29 – Grammar production definitions

| Form | Meaning |
|------|--------|
| `NonterminalElement : AbstractSyntaxElement = ...` | Production that synthesizes AbstractSyntaxElement |
| `NonterminalElement (p : Type) : AbstractSyntaxElement = ...` | Parameterized production; parameter p of type Type |

---

## 2. Lexical structure

The lexical structure of the SysML textual notation is **identical to KerML** ([KerML] spec) **except**:

### 2.1 Reserved keywords (SysML)

```
about abstract accept action actor after alias all allocate allocation analysis
and as assert assign assume at attribute bind binding by calc case comment
concern connect connection constant constraint crosses decide def default
defined dependency derived do doc else end entry enum event exhibit exit expose
false filter first flow for fork frame from hastype if implies import in include
individual inout interface istype item join language library locale loop merge
message meta metadata nonunique not null objective occurrence of or ordered out
package parallel part perform port private protected public redefines ref
references render rendering rep require requirement return satisfy send snapshot
specializes stakeholder standard state subject subsets succession terminate then
timeslice to transition true until use variant variation verification verify via
view viewpoint when while xor
```

### 2.2 Special lexical terminals (keyword or symbol)

| Terminal | Equivalence |
|----------|-------------|
| `DEFINED_BY` | `':'` \| `'defined' 'by'` |
| `SPECIALIZES` | `':>'` \| `'specializes'` |
| `SUBSETS` | `':>'` \| `'subsets'` |
| `REFERENCES` | `'::>'` \| `'references'` |
| `CROSSES` | `'=>'` \| `'crosses'` |
| `REDEFINES` | `':>>'` \| `'redefines'` |

**Note:** Full lexical rules (NAME, STRING_VALUE, REGULAR_COMMENT, etc.) are defined in the KerML specification; SysML defers to KerML for those.

---

## 3. Textual notation productions (Section 8.2.2)

### 3.1 Elements and relationships (8.2.2.2)

```
Identification : Element =
  ( '<' declaredShortName = NAME '>' )?
  ( declaredName = NAME )?

RelationshipBody : Relationship =
  ';' | '{' ( ownedRelationship += OwnedAnnotation )* '}'
```

### 3.2 Dependencies (8.2.2.3)

```
Dependency =
  ( ownedRelationship += PrefixMetadataAnnotation )*
  'dependency' DependencyDeclaration
  RelationshipBody

DependencyDeclaration =
  ( Identification 'from' )?
  client += [QualifiedName] ( ',' client += [QualifiedName] )* 'to'
  supplier += [QualifiedName] ( ',' supplier += [QualifiedName] )*
```

### 3.3 Annotations (8.2.2.4)

```
Annotation =
  annotatedElement = [QualifiedName]
  OwnedAnnotation : Annotation = ownedRelatedElement += AnnotatingElement
AnnotatingMember : OwningMembership = ownedRelatedElement += AnnotatingElement
AnnotatingElement = Comment | Documentation | TextualRepresentation | MetadataFeature

Comment =
  ( 'comment' Identification ( 'about' ownedRelationship += Annotation ( ',' ownedRelationship += Annotation )* )? )?
  ( 'locale' locale = STRING_VALUE )? body = REGULAR_COMMENT

Documentation =
  'doc' Identification ( 'locale' locale = STRING_VALUE )? body = REGULAR_COMMENT

TextualRepresentation =
  ( 'rep' Identification )? 'language' language = STRING_VALUE body = REGULAR_COMMENT
```

### 3.4 Namespaces and packages (8.2.2.5)

```
RootNamespace : Namespace = PackageBodyElement*

Package =
  ( ownedRelationship += PrefixMetadataMember )*
  PackageDeclaration PackageBody

LibraryPackage =
  ( isStandard ?= 'standard' ) 'library'
  ( ownedRelationship += PrefixMetadataMember )*
  PackageDeclaration PackageBody

PackageDeclaration : Package = 'package' Identification
PackageBody : Package = ';' | '{' PackageBodyElement* '}'

PackageBodyElement : Package =
  ownedRelationship += PackageMember
  | ownedRelationship += ElementFilterMember
  | ownedRelationship += AliasMember
  | ownedRelationship += Import

MemberPrefix : Membership = ( visibility = VisibilityIndicator )?
PackageMember : OwningMembership = MemberPrefix ( ownedRelatedElement += DefinitionElement | ownedRelatedElement = UsageElement )

ElementFilterMember : ElementFilterMembership = MemberPrefix 'filter' ownedRelatedElement += OwnedExpression ';'

AliasMember : Membership =
  MemberPrefix 'alias' ( '<' memberShortName = NAME '>' )? ( memberName = NAME )? 'for' memberElement = [QualifiedName] RelationshipBody

Import =
  visibility = VisibilityIndicator 'import' ( isImportAll ?= 'all' )? ImportDeclaration RelationshipBody

ImportDeclaration : Import = MembershipImport | NamespaceImport
MembershipImport = importedMembership = [QualifiedName] ( '::' isRecursive ?= '**' )?
NamespaceImport = importedNamespace = [QualifiedName] '::' '*' ( '::' isRecursive ?= '**' )?
  | importedNamespace = FilterPackage { ownedRelatedElement += importedNamespace }

FilterPackage : Package = ownedRelationship += FilterPackageImport ( ownedRelationship += FilterPackageMember )+
FilterPackageMember : ElementFilterMembership = '[' ownedRelatedElement += OwnedExpression ']'

VisibilityIndicator : VisibilityKind = 'public' | 'private' | 'protected'
```

DefinitionElement and UsageElement enumerate all definition/usage kinds (Package, LibraryPackage, AttributeDefinition, EnumerationDefinition, …, ExtendedDefinition; NonOccurrenceUsageElement | OccurrenceUsageElement). See spec 8.2.2.5.2.

### 3.5 Definition and usage (8.2.2.6)

```
BasicDefinitionPrefix = isAbstract ?= 'abstract' | isVariation ?= 'variation'
DefinitionExtensionKeyword : Definition = ownedRelationship += PrefixMetadataMember
DefinitionPrefix : Definition = BasicDefinitionPrefix? DefinitionExtensionKeyword*

Definition = DefinitionDeclaration DefinitionBody
DefinitionDeclaration : Definition = Identification SubclassificationPart?
DefinitionBody : Type = ';' | '{' DefinitionBodyItem* '}'

DefinitionBodyItem : Type =
  ownedRelationship += DefinitionMember
  | ownedRelationship += VariantUsageMember
  | ownedRelationship += NonOccurrenceUsageMember
  | ( ownedRelationship += SourceSuccessionMember )? ownedRelationship += OccurrenceUsageMember
  | ownedRelationship += AliasMember
  | ownedRelationship += Import

DefinitionMember : OwningMembership = MemberPrefix ownedRelatedElement += DefinitionElement
VariantUsageMember : VariantMembership = MemberPrefix 'variant' ownedVariantUsage = VariantUsageElement
NonOccurrenceUsageMember : FeatureMembership = MemberPrefix ownedRelatedElement += NonOccurrenceUsageElement
OccurrenceUsageMember : FeatureMembership = MemberPrefix ownedRelatedElement += OccurrenceUsageElement

FeatureDirection : FeatureDirectionKind = 'in' | 'out' | 'inout'
RefPrefix : Usage =
  ( direction = FeatureDirection )? ( isDerived ?= 'derived' )?
  ( isAbstract ?= 'abstract' | isVariation ?= 'variation' )? ( isConstant ?= 'constant' )?
BasicUsagePrefix : Usage = RefPrefix ( isReference ?= 'ref' )?
EndUsagePrefix : Usage = isEnd ?= 'end' ( ownedRelationship += OwnedCrossFeatureMember )?
OwnedCrossFeatureMember : OwningMembership = ownedRelatedElement += OwnedCrossFeature
OwnedCrossFeature : ReferenceUsage = BasicUsagePrefix UsageDeclaration
UsageExtensionKeyword : Usage = ownedRelationship += PrefixMetadataMember
UnextendedUsagePrefix : Usage = EndUsagePrefix | BasicUsagePrefix
UsagePrefix : Usage = UnextendedUsagePrefix UsageExtensionKeyword*

Usage = UsageDeclaration UsageCompletion
UsageDeclaration : Usage = Identification FeatureSpecializationPart?
UsageCompletion : Usage = ValuePart? UsageBody
UsageBody : Usage = DefinitionBody
ValuePart : Feature = ownedRelationship += FeatureValue
FeatureValue = ( '=' | isInitial ?= ':=' | isDefault ?= 'default' ( '=' | isInitial ?= ':=' )? ) ownedRelatedElement += OwnedExpression

DefaultReferenceUsage : ReferenceUsage = RefPrefix Usage
ReferenceUsage = ( EndUsagePrefix | RefPrefix ) 'ref' Usage
VariantReference : ReferenceUsage = ownedRelationship += OwnedReferenceSubsetting FeatureSpecialization* UsageBody
```

SubclassificationPart, FeatureSpecializationPart, Typings, Subsets, References, Crosses, Redefinitions, MultiplicityPart, OwnedMultiplicity, MultiplicityRange, etc. — see spec 8.2.2.6.5 and 8.2.2.6.6. NonOccurrenceUsageElement and OccurrenceUsageElement list all usage kinds (ReferenceUsage, AttributeUsage, …, PartUsage, ActionUsage, etc.).

### 3.6 Attributes (8.2.2.7)

```
AttributeDefinition : AttributeDefinition = DefinitionPrefix 'attribute' 'def' Definition
AttributeUsage : AttributeUsage = UsagePrefix 'attribute' Usage
```

### 3.7 Enumerations (8.2.2.8)

```
EnumerationDefinition = DefinitionExtensionKeyword* 'enum' 'def' DefinitionDeclaration EnumerationBody
EnumerationBody : EnumerationDefinition = ';' | '{' ( ownedRelationship += AnnotatingMember | ownedRelationship += EnumerationUsageMember )* '}'
EnumerationUsageMember : VariantMembership = MemberPrefix ownedRelatedElement += EnumeratedValue
EnumeratedValue : EnumerationUsage = 'enum'? Usage
EnumerationUsage : EnumerationUsage = UsagePrefix 'enum' Usage
```

### 3.8 Occurrences (8.2.2.9)

```
OccurrenceDefinitionPrefix : OccurrenceDefinition =
  BasicDefinitionPrefix? ( isIndividual ?= 'individual' ownedRelationship += EmptyMultiplicityMember )? DefinitionExtensionKeyword*

OccurrenceDefinition = OccurrenceDefinitionPrefix 'occurrence' 'def' Definition
IndividualDefinition : OccurrenceDefinition = BasicDefinitionPrefix? isIndividual ?= 'individual' DefinitionExtensionKeyword* 'def' Definition ownedRelationship += EmptyMultiplicityMember
EmptyMultiplicityMember : OwningMembership = ownedRelatedElement += EmptyMultiplicity
EmptyMultiplicity : Multiplicity = { }

OccurrenceUsagePrefix : OccurrenceUsage =
  BasicUsagePrefix ( isIndividual ?= 'individual' )?
  ( portionKind = PortionKind { isPortion = true } )? UsageExtensionKeyword*

OccurrenceUsage = OccurrenceUsagePrefix 'occurrence' Usage
IndividualUsage : OccurrenceUsage = BasicUsagePrefix isIndividual ?= 'individual' UsageExtensionKeyword* Usage
PortionUsage : OccurrenceUsage = BasicUsagePrefix ( isIndividual ?= 'individual' )? portionKind = PortionKind UsageExtensionKeyword* Usage { isPortion = true }
PortionKind = 'snapshot' | 'timeslice'

EventOccurrenceUsage =
  OccurrenceUsagePrefix 'event'
  ( ownedRelationship += OwnedReferenceSubsetting FeatureSpecializationPart? | 'occurrence' UsageDeclaration? )
  UsageCompletion

SourceSuccessionMember : FeatureMembership = 'then' ownedRelatedElement += SourceSuccession
SourceSuccession : SuccessionAsUsage = ownedRelationship += SourceEndMember
SourceEndMember : EndFeatureMembership = ownedRelatedElement += SourceEnd
SourceEnd : ReferenceUsage = ( ownedRelationship += OwnedMultiplicity )?
```

### 3.9 Items (8.2.2.10)

```
ItemDefinition = OccurrenceDefinitionPrefix 'item' 'def' Definition
ItemUsage = OccurrenceUsagePrefix 'item' Usage
```

### 3.10 Parts (8.2.2.11)

```
PartDefinition = OccurrenceDefinitionPrefix 'part' 'def' Definition
PartUsage = OccurrenceUsagePrefix 'part' Usage
```

### 3.11 Ports (8.2.2.12)

```
PortDefinition =
  DefinitionPrefix 'port' 'def' Definition
  ownedRelationship += ConjugatedPortDefinitionMember
  { conjugatedPortDefinition.ownedPortConjugator.originalPortDefinition = this }

ConjugatedPortDefinitionMember : OwningMembership = ownedRelatedElement += ConjugatedPortDefinition
ConjugatedPortDefinition = ownedRelationship += PortConjugation
PortConjugation = { }

PortUsage = OccurrenceUsagePrefix 'port' Usage
ConjugatedPortTyping : ConjugatedPortTyping = '~' originalPortDefinition = ~[QualifiedName]
```

### 3.12 Connections (8.2.2.13)

```
ConnectionDefinition = OccurrenceDefinitionPrefix 'connection' 'def' Definition

ConnectionUsage =
  OccurrenceUsagePrefix
  ( 'connection' UsageDeclaration ValuePart? ( 'connect' ConnectorPart )? | 'connect' ConnectorPart )
  UsageBody

ConnectorPart : ConnectionUsage = BinaryConnectorPart | NaryConnectorPart
BinaryConnectorPart : ConnectionUsage = ownedRelationship += ConnectorEndMember 'to' ownedRelationship += ConnectorEndMember
NaryConnectorPart : ConnectionUsage = '(' ownedRelationship += ConnectorEndMember ',' ownedRelationship += ConnectorEndMember ( ',' ownedRelationship += ConnectorEndMember )* ')'
ConnectorEndMember : EndFeatureMembership = ownedRelatedElement += ConnectorEnd
ConnectorEnd : ReferenceUsage = ( ownedRelationship += OwnedCrossMultiplicityMember )? ( declaredName = NAME REFERENCES )? ownedRelationship += OwnedReferenceSubsetting
OwnedCrossMultiplicityMember : OwningMembership = ownedRelatedElement += OwnedCrossMultiplicity
OwnedCrossMultiplicity : Feature = ownedRelationship += OwnedMultiplicity

BindingConnectorAsUsage =
  UsagePrefix ( 'binding' UsageDeclaration )?
  'bind' ownedRelationship += ConnectorEndMember '=' ownedRelationship += ConnectorEndMember
  UsageBody

SuccessionAsUsage =
  UsagePrefix ( 'succession' UsageDeclaration )?
  'first' ownedRelationship += ConnectorEndMember 'then' ownedRelationship += ConnectorEndMember
  UsageBody
```

### 3.13 Interfaces (8.2.2.14)

```
InterfaceDefinition = OccurrenceDefinitionPrefix 'interface' 'def' DefinitionDeclaration InterfaceBody
InterfaceBody : Type = ';' | '{' InterfaceBodyItem* '}'
InterfaceBodyItem : Type = ownedRelationship += DefinitionMember | ownedRelationship += VariantUsageMember | ownedRelationship += InterfaceNonOccurrenceUsageMember | ( ownedRelationship += SourceSuccessionMember )? ownedRelationship += InterfaceOccurrenceUsageMember | ownedRelationship += AliasMember | ownedRelationship += Import
InterfaceNonOccurrenceUsageMember : FeatureMembership = MemberPrefix ownedRelatedElement += InterfaceNonOccurrenceUsageElement
InterfaceNonOccurrenceUsageElement : Usage = ReferenceUsage | AttributeUsage | EnumerationUsage | BindingConnectorAsUsage | SuccessionAsUsage
InterfaceOccurrenceUsageMember : FeatureMembership = MemberPrefix ownedRelatedElement += InterfaceOccurrenceUsageElement
InterfaceOccurrenceUsageElement : Usage = DefaultInterfaceEnd | StructureUsageElement | BehaviorUsageElement
DefaultInterfaceEnd : PortUsage = isEnd ?= 'end' Usage

InterfaceUsage = OccurrenceUsagePrefix 'interface' InterfaceUsageDeclaration InterfaceBody
InterfaceUsageDeclaration : InterfaceUsage = UsageDeclaration ValuePart? ( 'connect' InterfacePart )? | InterfacePart
InterfacePart : InterfaceUsage = BinaryInterfacePart | NaryInterfacePart
BinaryInterfacePart : InterfaceUsage = ownedRelationship += InterfaceEndMember 'to' ownedRelationship += InterfaceEndMember
NaryInterfacePart : InterfaceUsage = '(' ownedRelationship += InterfaceEndMember ',' ownedRelationship += InterfaceEndMember ( ',' ownedRelationship += InterfaceEndMember )* ')'
InterfaceEndMember : EndFeatureMembership = ownedRelatedElement += InterfaceEnd
InterfaceEnd : PortUsage = ( ownedRelationship += OwnedCrossMultiplicityMember )? ( declaredName = NAME REFERENCES )? ownedRelationship += OwnedReferenceSubsetting
```

### 3.14 Allocations (8.2.2.15)

```
AllocationDefinition = OccurrenceDefinitionPrefix 'allocation' 'def' Definition
AllocationUsage = OccurrenceUsagePrefix AllocationUsageDeclaration UsageBody
AllocationUsageDeclaration : AllocationUsage = 'allocation' UsageDeclaration ( 'allocate' ConnectorPart )? | 'allocate' ConnectorPart
```

### 3.15 Flows (8.2.2.16)

```
FlowDefinition : OccurrenceDefinitionPrefix 'flow' 'def' Definition

Message : FlowUsage = OccurrenceUsagePrefix 'message' MessageDeclaration DefinitionBody { isAbstract = true }
MessageDeclaration : FlowUsage =
  UsageDeclaration ValuePart? ( 'of' ownedRelationship += FlowPayloadFeatureMember )?
  ( 'from' ownedRelationship += MessageEventMember 'to' ownedRelationship += MessageEventMember )?
  | ownedRelationship += MessageEventMember 'to' ownedRelationship += MessageEventMember
MessageEventMember : ParameterMembership = ownedRelatedElement += MessageEvent
MessageEvent : EventOccurrenceUsage = ownedRelationship += OwnedReferenceSubsetting

FlowUsage = OccurrenceUsagePrefix 'flow' FlowDeclaration DefinitionBody
SuccessionFlowUsage = OccurrenceUsagePrefix 'succession' 'flow' FlowDeclaration DefinitionBody
FlowDeclaration : FlowUsage = UsageDeclaration ValuePart? ( 'of' ownedRelationship += FlowPayloadFeatureMember )? ( 'from' ownedRelationship += FlowEndMember 'to' ownedRelationship += FlowEndMember )? | ownedRelationship += FlowEndMember 'to' ownedRelationship += FlowEndMember
FlowPayloadFeatureMember : FeatureMembership = ownedRelatedElement += FlowPayloadFeature
FlowPayloadFeature : PayloadFeature = PayloadFeature
PayloadFeature : Feature = Identification? PayloadFeatureSpecializationPart ValuePart? | ownedRelationship += OwnedFeatureTyping ( ownedRelationship += OwnedMultiplicity )? | ownedRelationship += OwnedMultiplicity ownedRelationship += OwnedFeatureTyping
PayloadFeatureSpecializationPart : Feature = ( -> FeatureSpecialization )+ MultiplicityPart? FeatureSpecialization* | MultiplicityPart FeatureSpecialization+
FlowEndMember : EndFeatureMembership = ownedRelatedElement += FlowEnd
FlowEnd = ( ownedRelationship += FlowEndSubsetting )? ownedRelationship += FlowFeatureMember
FlowEndSubsetting : ReferenceSubsetting = referencedFeature = [QualifiedName] | referencedFeature = FeatureChainPrefix { ownedRelatedElement += referencedFeature }
FeatureChainPrefix : Feature = ( ownedRelationship += OwnedFeatureChaining '.' )+ ownedRelationship += OwnedFeatureChaining '.'
FlowFeatureMember : FeatureMembership = ownedRelatedElement += FlowFeature
FlowFeature : ReferenceUsage = ownedRelationship += FlowFeatureRedefinition
FlowFeatureRedefinition : Redefinition = redefinedFeature = [QualifiedName]
```

### 3.16 Actions (8.2.2.17)

```
ActionDefinition = OccurrenceDefinitionPrefix 'action' 'def' DefinitionDeclaration ActionBody
ActionBody : Type = ';' | '{' ActionBodyItem* '}'
ActionBodyItem : Type =
  NonBehaviorBodyItem
  | ownedRelationship += InitialNodeMember ( ownedRelationship += ActionTargetSuccessionMember )*
  | ( ownedRelationship += SourceSuccessionMember )? ownedRelationship += ActionBehaviorMember ( ownedRelationship += ActionTargetSuccessionMember )*
  | ownedRelationship += GuardedSuccessionMember
NonBehaviorBodyItem = ownedRelationship += Import | ownedRelationship += AliasMember | ownedRelationship += DefinitionMember | ownedRelationship += VariantUsageMember | ownedRelationship += NonOccurrenceUsageMember | ( ownedRelationship += SourceSuccessionMember )? ownedRelationship += StructureUsageMember
ActionBehaviorMember : FeatureMembership = BehaviorUsageMember | ActionNodeMember
InitialNodeMember : FeatureMembership = MemberPrefix 'first' memberFeature = [QualifiedName] RelationshipBody
ActionNodeMember : FeatureMembership = MemberPrefix ownedRelatedElement += ActionNode
ActionTargetSuccessionMember : FeatureMembership = MemberPrefix ownedRelatedElement += ActionTargetSuccession
GuardedSuccessionMember : FeatureMembership = MemberPrefix ownedRelatedElement += GuardedSuccession

ActionUsage = OccurrenceUsagePrefix 'action' ActionUsageDeclaration ActionBody
ActionUsageDeclaration : ActionUsage = UsageDeclaration ValuePart?

PerformActionUsage = OccurrenceUsagePrefix 'perform' PerformActionUsageDeclaration ActionBody
PerformActionUsageDeclaration : PerformActionUsage = ( ownedRelationship += OwnedReferenceSubsetting FeatureSpecializationPart? | 'action' UsageDeclaration ) ValuePart?

ActionNode : ActionUsage = ControlNode | SendNode | AcceptNode | AssignmentNode | TerminateNode | IfNode | WhileLoopNode | ForLoopNode
ActionNodeUsageDeclaration : ActionUsage = 'action' UsageDeclaration?
ActionNodePrefix : ActionUsage = OccurrenceUsagePrefix ActionNodeUsageDeclaration?

ControlNode = MergeNode | DecisionNode | JoinNode | ForkNode
ControlNodePrefix : OccurrenceUsage = RefPrefix ( isIndividual ?= 'individual' )? ( portionKind = PortionKind { isPortion = true } )? UsageExtensionKeyword*
MergeNode = ControlNodePrefix isComposite ?= 'merge' UsageDeclaration ActionBody
DecisionNode = ControlNodePrefix isComposite ?= 'decide' UsageDeclaration ActionBody
JoinNode = ControlNodePrefix isComposite ?= 'join' UsageDeclaration ActionBody
ForkNode = ControlNodePrefix isComposite ?= 'fork' UsageDeclaration ActionBody

AcceptNode : AcceptActionUsage = OccurrenceUsagePrefix AcceptNodeDeclaration ActionBody
AcceptNodeDeclaration : AcceptActionUsage = ActionNodeUsageDeclaration? 'accept' AcceptParameterPart
AcceptParameterPart : AcceptActionUsage = ownedRelationship += PayloadParameterMember ( 'via' ownedRelationship += NodeParameterMember )?
PayloadParameterMember : ParameterMembership = ownedRelatedElement += PayloadParameter
PayloadParameter : ReferenceUsage = PayloadFeature | Identification PayloadFeatureSpecializationPart? TriggerValuePart
TriggerValuePart : Feature = ownedRelationship += TriggerFeatureValue
TriggerFeatureValue : FeatureValue = ownedRelatedElement += TriggerExpression
TriggerExpression : TriggerInvocationExpression = kind = ( 'at' | 'after' ) ownedRelationship += ArgumentMember | kind = 'when' ownedRelationship += ArgumentExpressionMember
ArgumentMember : ParameterMembership = ownedMemberParameter = Argument
Argument : Feature = ownedRelationship += ArgumentValue
ArgumentValue : FeatureValue = value = OwnedExpression
ArgumentExpressionMember : ParameterMembership = ownedRelatedElement += ArgumentExpression
ArgumentExpression : Feature = ownedRelationship += ArgumentExpressionValue
ArgumentExpressionValue : FeatureValue = ownedRelatedElement += OwnedExpressionReference

SendNode : SendActionUsage = OccurrenceUsagePrefix ActionUsageDeclaration? 'send' ( ownedRelationship += NodeParameterMember SenderReceiverPart? | ownedRelationship += EmptyParameterMember SendReceiverPart )? ActionBody
SendNodeDeclaration : SendActionUsage = ActionNodeUsageDeclaration? 'send' ownedRelationship += NodeParameterMember SenderReceiverPart?
SenderReceiverPart : SendActionUsage = 'via' ownedRelationship += NodeParameterMember ( 'to' ownedRelationship += NodeParameterMember )? | ownedRelationship += EmptyParameterMember 'to' ownedRelationship += NodeParameterMember
NodeParameterMember : ParameterMembership = ownedRelatedElement += NodeParameter
NodeParameter : ReferenceUsage = ownedRelationship += FeatureBinding
FeatureBinding : FeatureValue = ownedRelatedElement += OwnedExpression
EmptyParameterMember : ParameterMembership = ownedRelatedElement += EmptyUsage
EmptyUsage : ReferenceUsage = { }

AssignmentNode : AssignmentActionUsage = OccurrenceUsagePrefix AssignmentNodeDeclaration ActionBody
AssignmentNodeDeclaration : ActionUsage = ( ActionNodeUsageDeclaration )? 'assign' ownedRelationship += AssignmentTargetMember ownedRelationship += FeatureChainMember ':=' ownedRelationship += NodeParameterMember
AssignmentTargetMember : ParameterMembership = ownedRelatedElement += AssignmentTargetParameter
AssignmentTargetParameter : ReferenceUsage = ( ownedRelationship += AssignmentTargetBinding '.' )?
AssignmentTargetBinding : FeatureValue = ownedRelatedElement += NonFeatureChainPrimaryExpression
FeatureChainMember : Membership = memberElement = [QualifiedName] | OwnedFeatureChainMember
OwnedFeatureChainMember : OwningMembership = ownedRelatedElement += OwnedFeatureChain

TerminateNode : TerminateActionUsage = OccurrenceUsagePrefix ActionNodeUsageDeclaration? 'terminate' ( ownedRelationship += NodeParameterMember )? ActionBody

IfNode : IfActionUsage = ActionNodePrefix 'if' ownedRelationship += ExpressionParameterMember ownedRelationship += ActionBodyParameterMember ( 'else' ownedRelationship += ( ActionBodyParameterMember | IfNodeParameterMember ) )?
ExpressionParameterMember : ParameterMembership = ownedRelatedElement += OwnedExpression
ActionBodyParameterMember : ParameterMembership = ownedRelatedElement += ActionBodyParameter
ActionBodyParameter : ActionUsage = ( 'action' UsageDeclaration? )? '{' ActionBodyItem* '}'
IfNodeParameterMember : ParameterMembership = ownedRelatedElement += IfNode

WhileLoopNode : WhileLoopActionUsage = ActionNodePrefix ( 'while' ownedRelationship += ExpressionParameterMember | 'loop' ownedRelationship += EmptyParameterMember ) ownedRelationship += ActionBodyParameterMember ( 'until' ownedRelationship += ExpressionParameterMember ';' )?

ForLoopNode : ForLoopActionUsage = ActionNodePrefix 'for' ownedRelationship += ForVariableDeclarationMember 'in' ownedRelationship += NodeParameterMember ownedRelationship += ActionBodyParameterMember
ForVariableDeclarationMember : FeatureMembership = ownedRelatedElement += UsageDeclaration
ForVariableDeclaration : ReferenceUsage = UsageDeclaration

ActionTargetSuccession : Usage = ( TargetSuccession | GuardedTargetSuccession | DefaultTargetSuccession ) UsageBody
TargetSuccession : SuccessionAsUsage = ownedRelationship += SourceEndMember 'then' ownedRelationship += ConnectorEndMember
GuardedTargetSuccession : TransitionUsage = ownedRelationship += GuardExpressionMember 'then' ownedRelationship += TransitionSuccessionMember
DefaultTargetSuccession : TransitionUsage = 'else' ownedRelationship += TransitionSuccessionMember
GuardedSuccession : TransitionUsage = ( 'succession' UsageDeclaration )? 'first' ownedRelationship += FeatureChainMember ownedRelationship += GuardExpressionMember 'then' ownedRelationship += TransitionSuccessionMember UsageBody
```

### 3.17 States (8.2.2.18)

```
StateDefinition = OccurrenceDefinitionPrefix 'state' 'def' DefinitionDeclaration StateDefBody
StateDefBody : StateDefinition = ';' | ( isParallel ?= 'parallel' )? '{' StateBodyItem* '}'
StateBodyItem : Type = NonBehaviorBodyItem | ( ownedRelationship += SourceSuccessionMember )? ownedRelationship += BehaviorUsageMember ( ownedRelationship += TargetTransitionUsageMember )* | ownedRelationship += TransitionUsageMember | ownedRelationship += EntryActionMember ( ownedRelationship += EntryTransitionMember )* | ownedRelationship += DoActionMember | ownedRelationship += ExitActionMember
EntryActionMember : StateSubactionMembership = MemberPrefix kind = 'entry' ownedRelatedElement += StateActionUsage
DoActionMember : StateSubactionMembership = MemberPrefix kind = 'do' ownedRelatedElement += StateActionUsage
ExitActionMember : StateSubactionMembership = MemberPrefix kind = 'exit' ownedRelatedElement += StateActionUsage
EntryTransitionMember : FeatureMembership = MemberPrefix ( ownedRelatedElement += GuardedTargetSuccession | 'then' ownedRelatedElement += TargetSuccession ) ';'
StateActionUsage : ActionUsage = EmptyActionUsage ';' | StatePerformActionUsage | StateAcceptActionUsage | StateSendActionUsage | StateAssignmentActionUsage
EmptyActionUsage : ActionUsage = { }
StatePerformActionUsage : PerformActionUsage = PerformActionUsageDeclaration ActionBody
StateAcceptActionUsage : AcceptActionUsage = AcceptNodeDeclaration ActionBody
StateSendActionUsage : SendActionUsage = SendNodeDeclaration ActionBody
StateAssignmentActionUsage : AssignmentActionUsage = AssignmentNodeDeclaration ActionBody
TransitionUsageMember : FeatureMembership = MemberPrefix ownedRelatedElement += TransitionUsage
TargetTransitionUsageMember : FeatureMembership = MemberPrefix ownedRelatedElement += TargetTransitionUsage

StateUsage = OccurrenceUsagePrefix 'state' ActionUsageDeclaration StateUsageBody
StateUsageBody : StateUsage = ';' | ( isParallel ?= 'parallel' )? '{' StateBodyItem* '}'
ExhibitStateUsage = OccurrenceUsagePrefix 'exhibit' ( ownedRelationship += OwnedReferenceSubsetting FeatureSpecializationPart? | 'state' UsageDeclaration ) ValuePart? StateUsageBody

TransitionUsage = 'transition' ( UsageDeclaration 'first' )? ownedRelationship += FeatureChainMember ownedRelationship += EmptyParameterMember ( ownedRelationship += EmptyParameterMember ownedRelationship += TriggerActionMember )? ( ownedRelationship += GuardExpressionMember )? ( ownedRelationship += EffectBehaviorMember )? 'then' ownedRelationship += TransitionSuccessionMember ActionBody
TargetTransitionUsage : TransitionUsage = ownedRelationship += EmptyParameterMember ( 'transition' ( ownedRelationship += EmptyParameterMember ownedRelationship += TriggerActionMember )? ( ownedRelationship += GuardExpressionMember )? ( ownedRelationship += EffectBehaviorMember )? | ... )? 'then' ownedRelationship += TransitionSuccessionMember ActionBody
TriggerActionMember : TransitionFeatureMembership = 'accept' { kind = 'trigger' } ownedRelatedElement += TriggerAction
TriggerAction : AcceptActionUsage = AcceptParameterPart
GuardExpressionMember : TransitionFeatureMembership = 'if' { kind = 'guard' } ownedRelatedElement += OwnedExpression
EffectBehaviorMember : TransitionFeatureMembership = 'do' { kind = 'effect' } ownedRelatedElement += EffectBehaviorUsage
EffectBehaviorUsage : ActionUsage = EmptyActionUsage | TransitionPerformActionUsage | TransitionAcceptActionUsage | TransitionSendActionUsage | TransitionAssignmentActionUsage
TransitionSuccessionMember : OwningMembership = ownedRelatedElement += TransitionSuccession
TransitionSuccession : Succession = ownedRelationship += EmptyEndMember ownedRelationship += ConnectorEndMember
EmptyEndMember : EndFeatureMembership = ownedRelatedElement += EmptyFeature
EmptyFeature : ReferenceUsage = { }
```

### 3.18 Calculations (8.2.2.19)

```
CalculationDefinition = OccurrenceDefinitionPrefix 'calc' 'def' DefinitionDeclaration CalculationBody
CalculationUsage : CalculationUsage = OccurrenceUsagePrefix 'calc' ActionUsageDeclaration CalculationBody
CalculationBody : Type = ';' | '{' CalculationBodyPart '}'
CalculationBodyPart : Type = CalculationBodyItem* ( ownedRelationship += ResultExpressionMember )?
CalculationBodyItem : Type = ActionBodyItem | ownedRelationship += ReturnParameterMember
ReturnParameterMember : ReturnParameterMembership = MemberPrefix? 'return' ownedRelatedElement += UsageElement
ResultExpressionMember : ResultExpressionMembership = MemberPrefix? ownedRelatedElement += OwnedExpression
```

### 3.19 Constraints (8.2.2.20)

```
ConstraintDefinition = OccurrenceDefinitionPrefix 'constraint' 'def' DefinitionDeclaration CalculationBody
ConstraintUsage = OccurrenceUsagePrefix 'constraint' ConstraintUsageDeclaration CalculationBody
AssertConstraintUsage = OccurrenceUsagePrefix 'assert' ( isNegated ?= 'not' )? ( ownedRelationship += OwnedReferenceSubsetting FeatureSpecializationPart? | 'constraint' ConstraintUsageDeclaration ) CalculationBody
ConstraintUsageDeclaration : ConstraintUsage = UsageDeclaration ValuePart?
```

### 3.20 Requirements (8.2.2.21)

```
RequirementDefinition = OccurrenceDefinitionPrefix 'requirement' 'def' DefinitionDeclaration RequirementBody
RequirementBody : Type = ';' | '{' RequirementBodyItem* '}'
RequirementBodyItem : Type = DefinitionBodyItem | ownedRelationship += SubjectMember | ownedRelationship += RequirementConstraintMember | ownedRelationship += FramedConcernMember | ownedRelationship += RequirementVerificationMember | ownedRelationship += ActorMember | ownedRelationship += StakeholderMember
SubjectMember : SubjectMembership = MemberPrefix ownedRelatedElement += SubjectUsage
SubjectUsage : ReferenceUsage = 'subject' UsageExtensionKeyword* Usage
RequirementConstraintMember : RequirementConstraintMembership = MemberPrefix? RequirementKind ownedRelatedElement += RequirementConstraintUsage
RequirementKind : RequirementConstraintMembership = 'assume' { kind = 'assumption' } | 'require' { kind = 'requirement' }
RequirementConstraintUsage : ConstraintUsage = ownedRelationship += OwnedReferenceSubsetting FeatureSpecializationPart? RequirementBody | ( UsageExtensionKeyword* 'constraint' | UsageExtensionKeyword+ ) ConstraintUsageDeclaration CalculationBody
FramedConcernMember : FramedConcernMembership = MemberPrefix? 'frame' ownedRelatedElement += FramedConcernUsage
FramedConcernUsage : ConcernUsage = ownedRelationship += OwnedReferenceSubsetting FeatureSpecializationPart? CalculationBody | ( UsageExtensionKeyword* 'concern' | UsageExtensionKeyword+ ) CalculationUsageDeclaration CalculationBody
ActorMember : ActorMembership = MemberPrefix ownedRelatedElement += ActorUsage
ActorUsage : PartUsage = 'actor' UsageExtensionKeyword* Usage
StakeholderMember : StakeholderMembership = MemberPrefix ownedRelatedElement += StakeholderUsage
StakeholderUsage : PartUsage = 'stakeholder' UsageExtensionKeyword* Usage

RequirementUsage = OccurrenceUsagePrefix 'requirement' ConstraintUsageDeclaration RequirementBody
SatisfyRequirementUsage = OccurrenceUsagePrefix 'assert' ( isNegated ?= 'not' ) 'satisfy' ( ownedRelationship += OwnedReferenceSubsetting FeatureSpecializationPart? | 'requirement' UsageDeclaration ) ValuePart? ( 'by' ownedRelationship += SatisfactionSubjectMember )? RequirementBody
SatisfactionSubjectMember : SubjectMembership = ownedRelatedElement += SatisfactionParameter
SatisfactionParameter : ReferenceUsage = ownedRelationship += SatisfactionFeatureValue
SatisfactionFeatureValue : FeatureValue = ownedRelatedElement += SatisfactionReferenceExpression
SatisfactionReferenceExpression : FeatureReferenceExpression = ownedRelationship += FeatureChainMember

ConcernDefinition = OccurrenceDefinitionPrefix 'concern' 'def' DefinitionDeclaration RequirementBody
ConcernUsage = OccurrenceUsagePrefix 'concern' ConstraintUsageDeclaration RequirementBody
```

### 3.21 Cases (8.2.2.22)

```
CaseDefinition = OccurrenceDefinitionPrefix 'case' 'def' DefinitionDeclaration CaseBody
CaseUsage = OccurrenceUsagePrefix 'case' ConstraintUsageDeclaration CaseBody
CaseBody : Type = ';' | '{' CaseBodyItem* ( ownedRelationship += ResultExpressionMember )? '}'
CaseBodyItem : Type = ActionBodyItem | ownedRelationship += SubjectMember | ownedRelationship += ActorMember | ownedRelationship += ObjectiveMember
ObjectiveMember : ObjectiveMembership = MemberPrefix 'objective' ownedRelatedElement += ObjectiveRequirementUsage
ObjectiveRequirementUsage : RequirementUsage = UsageExtensionKeyword* ConstraintUsageDeclaration RequirementBody
```

### 3.22 Analysis cases (8.2.2.23)

```
AnalysisCaseDefinition = OccurrenceDefinitionPrefix 'analysis' 'def' DefinitionDeclaration CaseBody
AnalysisCaseUsage = OccurrenceUsagePrefix 'analysis' ConstraintUsageDeclaration CaseBody
```

### 3.23 Verification cases (8.2.2.24)

```
VerificationCaseDefinition = OccurrenceDefinitionPrefix 'verification' 'def' DefinitionDeclaration CaseBody
VerificationCaseUsage = OccurrenceUsagePrefix 'verification' ConstraintUsageDeclaration CaseBody
RequirementVerificationMember : RequirementVerificationMembership = MemberPrefix 'verify' { kind = 'requirement' } ownedRelatedElement += RequirementVerificationUsage
RequirementVerificationUsage : RequirementUsage = ownedRelationship += OwnedReferenceSubsetting FeatureSpecialization* RequirementBody | ( UsageExtensionKeyword* 'requirement' | UsageExtensionKeyword+ ) ConstraintUsageDeclaration RequirementBody
```

### 3.24 Use cases (8.2.2.25)

```
UseCaseDefinition = OccurrenceDefinitionPrefix 'use' 'case' 'def' DefinitionDeclaration CaseBody
UseCaseUsage = OccurrenceUsagePrefix 'use' 'case' ConstraintUsageDeclaration CaseBody
IncludeUseCaseUsage : OccurrenceUsagePrefix 'include' ( ownedRelationship += OwnedReferenceSubsetting FeatureSpecializationPart? | 'use' 'case' UsageDeclaration ) ValuePart? CaseBody
```

### 3.25 Views and viewpoints (8.2.2.26)

```
ViewDefinition = OccurrenceDefinitionPrefix 'view' 'def' DefinitionDeclaration ViewDefinitionBody
ViewDefinitionBody : ViewDefinition = ';' | '{' ViewDefinitionBodyItem* '}'
ViewDefinitionBodyItem : ViewDefinition = DefinitionBodyItem | ownedRelationship += ElementFilterMember | ownedRelationship += ViewRenderingMember
ViewRenderingMember : ViewRenderingMembership = MemberPrefix 'render' ownedRelatedElement += ViewRenderingUsage
ViewRenderingUsage : RenderingUsage = ownedRelationship += OwnedReferenceSubsetting FeatureSpecializationPart? UsageBody | ( UsageExtensionKeyword* 'rendering' | UsageExtensionKeyword+ ) Usage

ViewUsage = OccurrenceUsagePrefix 'view' UsageDeclaration? ValuePart? ViewBody
ViewBody : ViewUsage = ';' | '{' ViewBodyItem* '}'
ViewBodyItem : ViewUsage = DefinitionBodyItem | ownedRelationship += ElementFilterMember | ownedRelationship += ViewRenderingMember | ownedRelationship += Expose
Expose = 'expose' ( MembershipExpose | NamespaceExpose ) RelationshipBody
MembershipExpose = MembershipImport
NamespaceExpose = NamespaceImport

ViewpointDefinition = OccurrenceDefinitionPrefix 'viewpoint' 'def' DefinitionDeclaration RequirementBody
ViewpointUsage = OccurrenceUsagePrefix 'viewpoint' ConstraintUsageDeclaration RequirementBody

RenderingDefinition = OccurrenceDefinitionPrefix 'rendering' 'def' Definition
RenderingUsage = OccurrenceUsagePrefix 'rendering' Usage
```

### 3.26 Metadata (8.2.2.27)

```
MetadataDefinition = ( isAbstract ?= 'abstract' )? DefinitionExtensionKeyword* 'metadata' 'def' Definition
PrefixMetadataAnnotation : Annotation = '#' annotatingElement = PrefixMetadataUsage { ownedRelatedElement += annotatingElement }
PrefixMetadataMember : OwningMembership = '#' ownedRelatedElement = PrefixMetadataUsage
PrefixMetadataUsage : MetadataUsage = UsageExtensionKeyword* ( '@' | 'metadata' ) MetadataUsageDeclaration ( 'about' ownedRelationship += Annotation ( ',' ownedRelationship += Annotation )* )? MetadataBody
MetadataUsageDeclaration : MetadataUsage = ( Identification ( ':' | 'typed' 'by' ) )? ownedRelationship += OwnedFeatureTyping
MetadataBody : Type = ';' | '{' ( ownedRelationship += DefinitionMember | ownedRelationship += MetadataBodyUsageMember | ownedRelationship += AliasMember | ownedRelationship += Import )* '}'
MetadataBodyUsageMember : FeatureMembership = ownedMemberFeature = MetadataBodyUsage
MetadataBodyUsage : ReferenceUsage : 'ref'? ( ':>>' | 'redefines' )? ownedRelationship += OwnedRedefinition FeatureSpecializationPart? ValuePart? MetadataBody

ExtendedDefinition : Definition = BasicDefinitionPrefix? DefinitionExtensionKeyword+ 'def' Definition
ExtendedUsage : Usage = UnextendedUsagePrefix UsageExtensionKeyword+ Usage
```

---

## 4. Graphical notation (Section 8.2.3)

The spec defines a **graphical BNF** (8.2.3) with the same EBNF conventions plus 2-D layout, shapes, and lines. Terminal text appears as `'terminal'` or `LEXICAL`. See the Language Specification Section 8.2.3 for the full graphical grammar (elements, dependencies, annotations, namespaces, definitions/usages, attributes, enumerations, occurrences, items, parts, ports, connections, interfaces, allocations, flows, actions, states, calculations, constraints, requirements, cases, analysis/verification/use cases, views/viewpoints, metadata).

---

## 5. References

- **OMG SysML v2.0** — [Part 1: Language](https://www.omg.org/spec/SysML/2.0/Language/) (formal/2025-09-03).
- **KerML** — Kernel Modeling Language specification (lexical structure and common elements); OMG KerML spec.
- **This workspace** — `sysml-v2-models/` uses this textual syntax; setup: [SYSML_V2_MCP_SETUP.md](../../../docs/mcp/SYSML_V2_MCP_SETUP.md).
