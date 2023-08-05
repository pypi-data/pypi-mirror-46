from django.test import *
from unittest import skipIf


class FactoryModelTestCase():
    def setUp(self, **kwargs):
        self.factory = kwargs['factory']
        self.model = self.factory._meta.model
        self.db_obj = self.factory()
        self.qs = self.model.objects.all()
        self.qs_count = self.model.objects.all()

    def test_model_exists(self):
        obj = self.db_obj

        ###
        # Test against the object in the database not whats in memory.
        db_obj = self.model.objects.filter(uuid=obj.uuid)
        self.assertTrue(db_obj.exists())
        ###

        db_obj = db_obj.first()

        ##
        # Confirm fresh customer model is what we expect.
        self.assertEqual(obj.uuid, db_obj.uuid)
        ##

    def test_model_create_batch(self):
        self.factory.create_batch(3)
