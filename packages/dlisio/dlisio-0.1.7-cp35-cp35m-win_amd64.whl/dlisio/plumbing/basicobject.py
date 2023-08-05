from .. import core
from .valuetypes import *

class BasicObject():
    """Basic object
    Python representation of the set of logical record types (listed in
    Appendix A - Logical Record Types, described in Chapter 5 - Static and
    Frame Data)

    All object-types are derived from BasicObject, but that is just a way of
    adding the object-name field which is present in every object, as well as
    specifying the object type. These two fields makes a unique indentifier for
    the object.
    """
    def __init__(self, obj, name = None, type = None):
        self._type      = type
        self.name       = None
        self.origin     = None
        self.copynumber = None
        self._attic     = obj

        try:
            self.name       = name.id
            self.origin     = int(name.origin)
            self.copynumber = int(name.copynumber)
        except AttributeError:
            pass

    def __repr__(self):
        return "dlisio.{}(id={}, origin={}, copynumber={})".format(
                self.type,
                self.name,
                self.origin,
                self.copynumber)

    def __str__(self):
        s  = "dlisio.{}:\n".format(self.type)
        for key, value in self.__dict__.items():
            s += "\t{}: {}\n".format(key, value)
        return s

    @property
    def fingerprint(self):
        """ Object fingerprint

        Return the fingerprint, a unique identifier, for this object. This is
        basically an objref type from the RP66 standard, but with a pythonic
        flavour, and suitable for keys in dicts.

        Returns
        -------

        fingerprint : str
        """
        return core.fingerprint(self.type,
                                self.name,
                                self.origin,
                                self.copynumber)

    @property
    def type(self):
        """ Type

        The type of the object. Together, the type- and name-attribute form a
        unique object-identifier across all objects in the Logical File

        Returns
        -------

        type : str
        """
        return self._type

    @property
    def attic(self):
        """ The original object as represented on disk

        Attic refers the underlying basic_object, which is a
        dict-representation of the data on disk. The attic can be None if this
        particular instance was not loaded from disk.

        Notes
        -----

        This attribute is mainly intended for debugging purpuses

        Returns
        -------

        attic : dl:basic_object
        """
        return self._attic

    def stripspaces(self):
        """Strip spaces

        Remove leading and trailing withspaces for object attributes as they
        may be padded with whitespaces.
        """
        for key, value in self.__dict__.items():
            if isinstance(value, str):
                self.__dict__[key] = value.strip()
            if isinstance(value, list):
                if not isinstance(value, str): continue
                for inx, v in enumerate(value):
                    self.__dict__[key][inx] = v.strip()

    def link(self, objects, sets):
        """ Link objects

        The default implementation is a no-op - individual object types
        themselves are aware on how to link to other objects
        """
        pass

    @classmethod
    def load(cls, obj, name = None):
        """Populate the Python object with values from the native c++ object.

        This is achieved by looping over the Python class' attribute list
        (which maps the native c++ attribute names to the attribute names in the
        Python class) and extracting the value(s). Essensially, this is whats
        going on:

        >>> for label, value in obj.items():
        ...     if label == 'LONG-NAME': self.long_name = value
        ...     if label == 'CHANNEL'  : self.channel   = value

        By using a classmethod, this process is generalized for all object
        types derived from basic_object.
        """
        self = cls(obj, name = name)

        attrs = cls.attributes
        for label, value in obj.items():
            if value is None: continue

            attr, value_type = attrs[label]
            if value_type == ValueTypeScalar:
                setattr(self, attr, value[0])

            elif value_type == ValueTypeVector:
                setattr(self, attr, value)

            elif value_type == ValueTypeBoolean:
                setattr(self, attr, bool(value[0]))

            else:
                problem = 'unknown value extraction descriptor {}'
                solution = 'should be either scalar, vector, or boolean'
                msg = ', '.join((problem.format(value_type), solution))
                raise ValueError(msg)


        self.stripspaces()
        return self
