# Guidelines

This document gives a a description of how the vocabulary can be used.

The EDPOP collection vocabulary is designed to describe annotated collections, primarily for research in the humanities. The vocabulary is agnostic about what collections should contain: you can think of books, films, scholarly articles or something else altogether. In the case of the EDPOP project, collections contain records in library catalogues.

### Aims

We can formulate several requirements for use in research:
- The vocabulary should recognise collections and annotations as intellectual labour which should have clear attribution. Users should be able to provide information about themselves and their work.
- The vocabulary should be able to express data updates and corrections in a non-destructive manner. It should be possible to view the history of corrections on a resource.
- When two researchers add the same resource to their respective collections, they should each be able to make their own annotations and corrections, without interfering with one another. At the same time, the graph should make it easy to query others' annotations on the same resource.

This last point may be surprising: researchers do not need to build towards a shared, singular source of truth. As a project, EDPOP is not an attempt to construct a singular RDF dataset, but rather a means for researchers from different projects to present their work.

- The abstraction and discretisation of data that graphs require consists of many non-trivial choices; what choices are appropriate often depends on the theoretical framework the researcher is working in, and the aims of their research project. When two researchers produce contradicting graphs, they may sometimes be understood not as disagreement, but as reliance on different models.
- In cases where researchers truly disagree, they must each be able to express their viewpoint; this can include a personal "container" where the researcher can work out exactly how they would encode the data.


## Agents

For the sake of attribution, we distinguish between two types of agents: users and applications. Users represent real people, who can be cited as authors. Applications represent software that interacts with the graph.

### Users

In an application, it makes sense to let user nodes correspond one-to-one with users in an authentication system. In that case, the user nodes function as the "public" face of the user; this is the way their contributions are attributed.

User nodes can have properties that describes the individual and their work. These should be defined by user themself.

A user may have no informative properties at all. This allows users to make pseudonymous contributions, where there is still a clear record of all contributions by that user.

### Applications

An application node represents a software application that makes contributions to the graph. These can be periodic updates or data migrations, which can be realised as annotations or direct changes.

Any user-created resource can also have an application as its `as:generator` - this just states that the application was used to make the contribution. That information can be somewhat useful when the graph is shared, as applications often restrict the created resource.

Automatically generated resources, e.g. automatic annotations, can be realised as annotations not attributed to users; such annotions should have an `as:generator` to describe their provenance.

## Collections

Collections have two functions:

- They present a collection of resources that a user has assembled
- They are the context in which users make annotations

In the most straightforward case, annotations are made on members of the collection. For example, a collection contains several books, and the owner of the collection has made annotations on those books.

Note that even this case, context and membership are different things. Consider the following graph:

```ttl
_:GreatAuthors a edpopcol:Collection .
_:Shakespeare rdfs:member _:GreatAuthors .

_:a1  a edpopcol:Annotation ;
    oa:hasTarget [ oa:hasSource _:Shakespeare ] .
```

While this may seem to imply that the annotation is made in the context of the `_:GreatAuthors` collection, it is possible that Shakespeare is a member of another collection, and the annotation was made in that context. Thus, we also need to specify:

```ttl
_:a1 as:context _:GreatAuthors .
```

It is not required that annotations target members of collections. It often makes sense to annotate resources that are indirectly related to members of the collection. In the example above, the user may want to annotate that Shakespeare's birthplace lies in England, by suggesting that `_:StratfordUponAvon _:country _:England` be added to the graph - but that triple is not directly related to the collection.


## Annotations

### Comments

Annotations can include comments. A minimal annotations is just making a comment, without any structured suggestions. For example:

```ttl
[]  a edpopcol:Annotation ;
    oa:motivatedBy oa:commenting ;
    oa:hasTarget [
        oa:hasSource _:Hamlet
    ] ;
    oa:hasBody [
        edpopcol:comment [
            a oa:TextualBody ;
            rdf:value "is this guy ever going to do anything?" ;
            dc:language: "en" ;
            dc:format "text/html"
        ]
    ] .
```

### Predicate selection

Annotations can include a `PredicateSelector` to their target resource, which indicates that the annotation is somehow "about" or "in response to" a particular property of the resource. 

This is especially useful for comments. Without a selector, a comment is understood as being about the resource as a whole; the selector restricts the domain which allows for more targeted comments.

```ttl
[]  a edpopcol:Annotation ;
    oa:motivatedBy oa:commenting ;
    oa:hasTarget [
        oa:hasSource _:Hamlet ;
        oa:hasSelector [
            edpopcol:property _:loves ;
            edpopcol:object _:Ophelia
        ]
    ] ;
    oa:hasBody [
        edpopcol:comment [
            a oa:TextualBody ;
            rdf:value "does he really?" ;
            dc:language: "en" ;
            dc:format "text/html"
        ]
    ] .
```

A reasoner may use this information to, for instance:

- place the comment within the view representation of "Hamlet loves Ophelia"
- classify the comment as outdated when `_:Hamlet _:loves _:Ophelia` is removed from the graph
- understand this as a comment that is not just related to `_:Hamlet`, but also related to `_:Ophelia`

The predicate selector may be partial, defining only a property or only an object. (Though the latter may be less sensible.) In the following example, the commenter restricts the scope of their comment to "things that Hamlet loves":

```ttl
[]  a edpopcol:Annotation ;
    oa:motivatedBy oa:commenting ;
    oa:hasTarget [
        oa:hasSource _:Hamlet ;
        oa:hasSelector [
            edpopcol:property _:loves
        ]
    ] ;
    oa:hasBody [
        edpopcol:comment [
            a oa:TextualBody ;
            rdf:value "he doesn't love anyone but himself!" ;
            dc:language: "en" ;
            dc:format "text/html"
        ]
    ] .
```

### Suggestions

Annotations can provide structured suggestions for the resource. There are two atomic suggestions:

- Add a triple
- Remove a triple

Combining these two allows any sort of edit.

EDPOP annotations have one restriction, which is that they are always about the same subject. Thus, a single annotation could suggest:

- Remove `_:Denmark _:king _:HamletSenior`
- Add `_:Denmark _:king _:Claudius`

But these suggestions would have to be done in separate annotations:

- Add `_:Claudius _:kingOf _:Denmark`
- Remove `_:HamletSenior _:kingOf _:Denmark`

It is generally recommended that annotations stick to a small number of coherent suggestions, but the vocabulary does not enforce this.

Suggestions can be added to the body of annotations through the `suggestsRemoval` and `suggestsAddition` properties. For example:

```ttl
[]  a edpopcol:Annotation ;
    oa:motivatedBy oa:commenting ;
    oa:hasTarget [
        oa:hasSource _:Denmark 
    ] ;
    oa:hasBody [
        edpopcol:suggestsRemoval [
            edpopcol:property _:king ;
            edpopcol:object _:HamletSenior
        ] ;
        edpopcol:suggestsAddition [
            edpopcol:property _:king ;
            edpopcol:object _:Claudius
        ]
    ] .
```

### Identifying

It can be useful to identify one resource with another, especially when annotating data from different sources. Identification is essentially an "add a property" annotation: the agent suggests setting `owl:sameAs`.

For instance, this annotations suggests that `_:Ghost` and `_:HamletSenior` are the same.

```ttl
[]  a edpopcol:Annotation ;
    oa:motivatedBy oa:identifying ;
    oa:hasTarget [
        oa:hasSource _:Ghost ;
    ] ;
    oa:hasBody [
        edpopcol:suggestsAddition [
            edpopcol:property owl:sameAs ;
            edpopcol:object _:HamletSenior
        ]
    ]
```

Note that the motivation of this annotation is `oa:identifying` rather than `oa:editing`.

### Suggestions and comments

Some notes about the relationship between suggestions and comments:

Annotation bodies may contain both suggestions and comments. By including both, an annotation can suggest new data while also including a comment explaining the reason for the correction.

The relationship between suggestions/comments in the body and the motivation is somewhat loose. It does not make much sense to make `oa:motivatedBy oa:editing` annotation without a suggestion.

However, it is conceivable to make a `oa:motivatedBy oa:commenting` annotation that also includes suggestions. In that case, the suggestions may be thought of as structured references to predicates, rather than propositions that those predicates hold for the subject. This could be used to express uncertainty, e.g. for annotations like "I think it's something like this". However, an application may ignore this possibility.

### Predicate selectors and predicate suggestions

We have seen that annotation targets can have a predicate selector and annotation bodies can make suggestions about predicates. It is therefore possible to make an annotation that has both, e.g.:

```ttl
[]  a edpopcol:Annotation ;
    oa:motivatedBy oa:editing ;
    oa:hasTarget [
        oa:hasSource _:Denmark ;
        oa:hasSelector [
            edpopcol:property _:king ;
            edpopcol:object _:HamletSenior
        ]
    ] ;
    oa:hasBody [
        edpopcol:suggestsRemoval [
            edpopcol:property _:king ;
            edpopcol:object _:HamletSenior
        ] ;
        edpopcol:suggestsAddition [
            edpopcol:property _:king ;
            edpopcol:object _:Claudius
        ]
    ] .
```

One could argue that the predicate selector is redundant: we can already read from the suggestion that this annotation is correcting the predicate `_:king _:HamletSenior`.

Nonetheless, it can be useful to include target selectors for suggestions. One reason is that the redundant information can make querying a bit easier. 

Note that the selector describes the current state of the graph: the annotation is reacting to the triple `_:Denmark _:king _:HamletSenior`. It should not select the suggested predicate `_:king _:Claudius`.

## Suggestions and changing the graph

Annotations can provide structured suggestions; whether these suggestions are accepted is another question.

#### Accepting corrections

It is useful to express that an annotation is regarded as canonical in a particular context. For instance, when a researcher makes corrections within their own collections, those may be regarded as canonical in that context. A reasoner could then use this status to create a unified, corrected graph.

At the moment, there is no implementation for this within the vocabulary, due to its complexity. Canonical status raises questions about moderation, and creating a unified graph is a non-trivial task, since annotations can contradict each other. 

### Suggestions vs. modifications

When can agents modify the graph, and when should they make annotations? It is theoretically possible to handle *everything* through annotations and enable only the following:

- allow agents to create blank subject nodes
- allow agents to make suggestions through annotations
- mark some annotations as canonical

However, this quickly becomes intractible. The complexity of reasoning over annotations to determine the "canonical" graph is not something you want to do for every single relationship. It makes more sense to limit annotations to the objects of research, while the management of users and collections is mainly done through direct modification on the graph.

Nonetheless, there is a balance between annotations and modifications that must be explored in implementation. 

### Annotation context

Annotations will usually have an `as:context` that indicates the collection in which this annotation is relevant. It is possible for an annotation to have multiple collections as context: this indicates that the collections is also deemed to be relevant in other collections.

It can be useful to also know the *original* context in which the annotation was made. The recommend way to include this information is add record of the original creation event, such as an `as:Create` node, which specifies the context.

```ttl
_:col a edpopcol:Collection .
_:col2 a edpopcol:Collection .

_:ann   a edpopcol:Annotation ;
        as:context _:col , _:col2 .

[]  a as:Create ;
    as:context _:col .
```

It is sometimes useful to make context-independent annotations that are always relevant in an research environment. The recommended way to handle this is to create a "universal collection" for the environment: an instance of `edpopcol:Collection` which is understood to be "relevant" or "active" regardless of context.

(A universal collection may exist without an `edpopcol:creator` - in fact, it may be the only collection without one. However, it is conceivable that a collection is considered universal while still having a creator, e.g. an admin).

### Replying to annotations

We often want to express that an annotation is reacting to some other annotation. 

In general, the recommendation is that this is done by having multiple annotations on the same resource, rather than by chaining annotations, with each annotations having another annotation as subject. This reduces the complexity of querying relevant annotations or reasoning about suggestions.

If desired, linking annotations can be done through relations like `as:inReplyTo`.

### Tracking changes

Annotations provide a clear language to say "this agent made this suggestion at this moment in time". It is recommended that, when modifications are made to the graph (or the domain within the graph that annotations are used on), these are tracked as well, for instance through the [activity streams vocabulary](https://www.w3.org/TR/activitystreams-vocabulary/). Thus, annotations exist alongside a record of changes.

This is because annotations provide a framework to express "this agent made this suggestion at this point in time". If the subject is also being updated over time, then it makes sense to also keep a record of those changes. Such a record can help to contextualise annotations, to mark that annotations became outdated after updates, or to understand interactions by having attribution for both the annotation and its target.
