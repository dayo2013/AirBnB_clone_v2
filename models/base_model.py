#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DATETIME
from models import storage_type

Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models"""

    id = Column(String(60),
                nullable=False,
                primary_key=True,
                unique=True)
    created_at = Column(DATETIME,
                        nullable=False,
                        default=datetime.utcnow())
    updated_at = Column(DATETIME,
                        nullable=False,
                        default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Instantiation of base model class
        Args:
            args: it won't be used
            kwargs: arguments for the constructor of the BaseModel
        Attributes:
            id: unique id generated
            created_at: creation date
            updated_at: updated date
        """
        if kwargs:
            if 'id' not in kwargs:
                self.id = str(uuid.uuid4())

            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                if key != "__class__":
                    setattr(self, key, value)

            if 'created_at' not in kwargs:
                self.created_at = self.updated_at = datetime.now()
        else:
            self.id = str(uuid.uuid4())

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dct = self.__dict__.copy()
        dct['__class__'] = self.__class__.__name__
        for k in dct:
            if type(dct[k]) is datetime:
                dct[k] = dct[k].isoformat()
        if '_sa_instance_state' in dct.keys():
            del (dct['_sa_instance_state'])
        return dct

    def delete(self):
        '''deletes the current instance from the storage'''
        from models import storage
        storage.delete(self)
