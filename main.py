from flask import Flask, render_template, request
import uuid
import re

app = Flask(__name__)

# In-memory storage for mapping UUID to semantic identifier
uuid_to_semantic_id = {}

class FisheryID:
    def __init__(self, species, area, authority, management_area, flag, gear):
        self.species = species
        self.area = area
        self.authority = authority
        self.management_area = management_area
        self.flag = flag
        self.gear = gear
        self.semantic_id = self.generate_semantic_identifier()
        self.uuid = self.generate_uuid()
        # Store the mapping in the in-memory storage
        uuid_to_semantic_id[self.uuid] = self.semantic_id

    def generate_semantic_identifier(self):
        return f"asfis:{self.species} +{self.area} + authority:{self.authority}: {self.flag}+ {self.management_area} + iso3:{self.flag}+isscfg:{self.gear}"

    def generate_uuid(self):
        return str(uuid.uuid5(uuid.NAMESPACE_URL, self.semantic_id))

    @staticmethod
    def parse_semantic_identifier(semantic_id):
        pattern = r"asfis:(\w+) \+(.+) \+ authority:(\w+): (\w+)\+ (.+) \+ iso3:(\w+)\+isscfg:(\w+)"
        match = re.match(pattern, semantic_id)
        if match:
            species, area, authority, flag, management_area, gear = match.groups()
            return FisheryID(species, area, authority, management_area, flag, gear)
        return None

    @staticmethod
    def get_semantic_id_from_uuid(uuid_str):
        return uuid_to_semantic_id.get(uuid_str)

@app.route('/', methods=['GET', 'POST'])
def index():
    created_id = None
    decoded_id = None
    uuid_id = None
    semantic_id_from_uuid = None
    decoded_fields = None
    if request.method == 'POST':
        if 'create' in request.form:
            fishery_id = FisheryID(
                request.form['species'],
                request.form['area'],
                request.form['authority'],
                request.form['management_area'],
                request.form['flag'],
                request.form['gear']
            )
            created_id = fishery_id.semantic_id
        elif 'decode' in request.form:
            semantic_id = request.form['semantic_id']
            decoded = FisheryID.parse_semantic_identifier(semantic_id)
            if decoded:
                decoded_id = {
                    'species': decoded.species,
                    'area': decoded.area,
                    'authority': decoded.authority,
                    'management_area': decoded.management_area,
                    'flag': decoded.flag,
                    'gear': decoded.gear
                }
                decoded_fields = {
                    'species': decoded.species,
                    'area': decoded.area,
                    'authority': decoded.authority,
                    'management_area': decoded.management_area,
                    'flag': decoded.flag,
                    'gear': decoded.gear
                }
        elif 'generate_uuid' in request.form:
            semantic_id = request.form['semantic_id']
            fishery_id = FisheryID.parse_semantic_identifier(semantic_id)
            if fishery_id:
                uuid_id = fishery_id.uuid
        elif 'get_semantic_id' in request.form:
            uuid_str = request.form['uuid']
            semantic_id_from_uuid = FisheryID.get_semantic_id_from_uuid(uuid_str)
    return render_template('index.html', created_id=created_id, decoded_id=decoded_id, uuid_id=uuid_id, semantic_id_from_uuid=semantic_id_from_uuid, decoded_fields=decoded_fields)

# No need for the if __name__ == '__main__': block when using Gunicorn
