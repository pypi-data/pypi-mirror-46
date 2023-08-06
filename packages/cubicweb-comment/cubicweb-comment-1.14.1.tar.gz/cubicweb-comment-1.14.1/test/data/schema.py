from yams.buildobjs import RelationDefinition

class comments(RelationDefinition):
    subject = 'Comment'
    object = ('CWUser', 'BlogEntry')
    cardinality = '1*'
    composite = 'object'
