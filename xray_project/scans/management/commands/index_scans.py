from django.core.management.base import BaseCommand
from scans.models import XRayScan

class Command(BaseCommand):
    help = 'Index all XRayScan records in Elasticsearch'

    def handle(self, *args, **options):
        try:
            from scans.documents import XRayScanDocument
            
            # Delete existing index if it exists
            try:
                XRayScanDocument._index.delete()
            except:
                pass
            
            # Create the index
            XRayScanDocument._index.create()
            
            # Index all scans
            scans = XRayScan.objects.all()
            count = 0
            
            for scan in scans:
                # Create document instance
                doc = XRayScanDocument(
                    meta={'id': scan.id},
                    patient_id=scan.patient_id,
                    body_part=scan.body_part,
                    scan_date=scan.scan_date,
                    institution=scan.institution,
                    description=scan.description,
                    diagnosis=scan.diagnosis,
                    tags=scan.tags
                )
                # Save to Elasticsearch
                doc.save()
                count += 1
                
            self.stdout.write(
                self.style.SUCCESS(f'Successfully indexed {count} scans')
            )
        except ImportError:
            self.stdout.write(
                self.style.WARNING('Elasticsearch is not configured. Skipping indexing.')
            )
        except Exception as e:
            if "Connection refused" in str(e):
                self.stdout.write(
                    self.style.ERROR('Error: Elasticsearch is not running.')
                )
                self.stdout.write(
                    self.style.NOTICE('To enable Elasticsearch functionality:')
                )
                self.stdout.write(
                    self.style.NOTICE('1. Download and install Elasticsearch from https://www.elastic.co/downloads/elasticsearch')
                )
                self.stdout.write(
                    self.style.NOTICE('2. Start Elasticsearch service')
                )
                self.stdout.write(
                    self.style.NOTICE('3. Run this command again')
                )
            else:
                self.stdout.write(
                    self.style.ERROR(f'Error indexing scans: {e}')
                )