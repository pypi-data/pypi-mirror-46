from . import digest as digest_
from . import regexp

ImageRegexps = regexp.ImageRegexps

NAME_TOTAL_LENGTH_MAX = 255


class InvalidReference(Exception):
    @classmethod
    def default(cls):
        return cls("invalid reference")


class ReferenceInvalidFormat(InvalidReference):
    @classmethod
    def default(cls):
        return cls("invalid reference format")


class TagInvalidFormat(InvalidReference):
    @classmethod
    def default(cls):
        return cls("invalid tag format")


class DigestInvalidFormat(InvalidReference):
    @classmethod
    def default(cls):
        return cls("invalid digest format")


class NameEmpty(InvalidReference):
    @classmethod
    def default(cls):
        return cls("repository name must have at least one component")


class NameTooLong(InvalidReference):
    @classmethod
    def default(cls):
        return cls("repository name must not be more than {} characters".format(NAME_TOTAL_LENGTH_MAX))


class Reference(dict):
    def __init__(self, name=None, tag=None, digest=None):
        super(Reference, self).__init__()
        self['name'] = name
        self['tag'] = tag
        self['digest'] = digest

    def split_hostname(self):
        name = self['name']
        matched = ImageRegexps.ANCHORED_NAME_REGEXP.match(name)

        if not matched:
            return '', name
        matches = matched.groups()
        if len(matches) != 2:
            return '', name

        return matches[0], matches[1]

    def string(self):
        return '{}:{}@{}'.format(self['name'], self['tag'], self['digest'])

    def best_reference(self):
        if not self['name']:
            if self['digest']:
                return DigestReference(self['digest'])
            return None

        if not self['tag']:
            if self['digest']:
                return CanonicalReference(self['name'], self['digest'])
            return NamedReference(self['name'])

        if not self['digest']:
            return TaggedReference(self['name'], self['tag'])

        return self

    @classmethod
    def try_validate(cls, s):
        if not s:
            raise NameEmpty.default()
        if '/' not in s:
            return
        hostname, _ = s.split('/', 1)
        matched = ImageRegexps.ANCHORED_HOSTNAME_REGEXP.match(hostname)
        if not matched:
            raise ReferenceInvalidFormat.default()

    @classmethod
    def parse(cls, s):
        cls.try_validate(s)

        matched = ImageRegexps.REFERENCE_REGEXP.match(s)
        if not matched:
            raise ReferenceInvalidFormat.default()

        matches = matched.groups()
        if len(matches[0]) > NAME_TOTAL_LENGTH_MAX:
            raise NameTooLong.default()

        ref = cls(name=matches[0], tag=matches[1])
        if matches[2]:
            digest_.validate_digest(matches[2])
            ref['digest'] = matches[2]

        r = ref.best_reference()
        if not r:
            raise NameEmpty.default()

        return r


class NamedReference(Reference):
    def __init__(self, name, **kwargs):
        super(NamedReference, self).__init__(name=name, **kwargs)

    def string(self):
        return '{}'.format(self['name'])


class DigestReference(Reference):
    def __init__(self, digest, **kwargs):
        super(DigestReference, self).__init__(digest=digest, **kwargs)

    def string(self):
        return self['digest']


class CanonicalReference(NamedReference):
    def __init__(self, name, digest, **kwargs):
        super(CanonicalReference, self).__init__(name=name, digest=digest, **kwargs)

    def string(self):
        return '{}@{}'.format(self['name'], self['digest'])


class TaggedReference(NamedReference):
    def __init__(self, name, tag, **kwargs):
        super(TaggedReference, self).__init__(name=name, tag=tag, **kwargs)

    def string(self):
        return '{}:{}'.format(self['name'], self['tag'])
