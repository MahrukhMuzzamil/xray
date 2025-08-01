from django_elasticsearch_dsl import Document, Index, fields
from django_elasticsearch_dsl.registries import registry
from .models import XRayScan

# Define the Elasticsearch index
xray_index = Index('xray_scans')
xray_index.settings(
    number_of_shards=1,
    number_of_replicas=0
)

@registry.register_document
class XRayScanDocument(Document):
    # Define fields for full-text search
    description = fields.TextField(
        attr='description',
        fields={
            'raw': fields.KeywordField(),
        }
    )
    
    diagnosis = fields.TextField(
        attr='diagnosis',
        fields={
            'raw': fields.KeywordField(),
        }
    )
    
    tags = fields.TextField(
        attr='tags',
        fields={
            'raw': fields.KeywordField(),
        }
    )
    
    body_part = fields.TextField(
        attr='body_part',
        fields={
            'raw': fields.KeywordField(),
        }
    )
    
    institution = fields.TextField(
        attr='institution',
        fields={
            'raw': fields.KeywordField(),
        }
    )
    
    class Index:
        # Name of the Elasticsearch index
        name = 'xray_scans'
        # See Elasticsearch Indices API reference for available settings
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }

    class Django:
        model = XRayScan  # The model associated with this Document

        # The fields of the model you want to be indexed in Elasticsearch
        fields = [
            'patient_id',
            'scan_date',
        ]