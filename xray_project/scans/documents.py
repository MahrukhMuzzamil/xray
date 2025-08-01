from django_elasticsearch_dsl import Document, Index, fields
from django_elasticsearch_dsl.registries import registry
from .models import XRayScan

xray_index = Index('xray_scans')
xray_index.settings(number_of_shards=1, number_of_replicas=0)

@registry.register_document
class XRayScanDocument(Document):
    description = fields.TextField()
    diagnosis = fields.TextField()
    tags = fields.TextField(multi=True)
    body_part = fields.TextField()
    institution = fields.TextField()

    class Index:
        name = 'xray_scans'
        settings = {'number_of_shards': 1, 'number_of_replicas': 0}

    class Django:
        model = XRayScan
        fields = ['patient_id', 'scan_date', 'image']
