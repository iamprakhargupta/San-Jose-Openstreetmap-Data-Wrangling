
#made by - prakhar gupta
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint
'''
These re expressions were tried on regex101.com Go the the url to view example of these expressions
'''

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE) # https://regex101.com/r/lqq9Fa/1
phone_no_7 = re.compile(r'^\d{7}$') # https://regex101.com/r/sk0amZ/1
phone_no_10 = re.compile(r'^\d{10}$') # https://regex101.com/r/lqq9Fa/2
phone_no_11 = re.compile(r'^\d{11}$') # https://regex101.com/r/lqq9Fa/3
POSTCODE = re.compile(r'^\d{5}$|\d{5}-\d{4}$') # https://regex101.com/r/lqq9Fa/4

expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Line", "Square", "Lane", "Road",
            "Trail", "Parkway", "North", "South", "West", "East", "Circle", "Gate", "Way"]

mapping = {
            "St": "Street",
            "St.": "Street",
            "STREET": "Street",
            "Ave": "Avenue",
            "Ave.": "Avenue",
            "Dr.": "Drive",
            "Dr": "Drive",
            "Rd": "Road",
            "Rd.": "Road",
            "Blvd": "Boulevard",
            "Blvd.": "Boulevard",
            "Ln": "Line",
            "Hwy":"Highway",
            "sq":"Square",
            "Ln.": "Line",
            "Trl": "Trail",
            "Cir": "Circle",
            "Cir.": "Circle",
            "Ct": "Court",
            "By-pass": "Bypass",
            "N": "North",
            "E": "East",
            "S": "South",
            "W": "West"
          }


def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit_street(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    return street_types


def update_street(name):
    '''
    Clean street name for insertion into CSV Files.Update_name takes ta name and checks it
    with mapping dict if it matches the mapping dict keys it substitute it with
    mapping dict values
    '''
    changed_name = name
    for key in mapping.keys():
      changed_name = re.sub(key, ' ' + mapping[key], changed_name)   
    # Check last words as avenue, road, street, etc. are capitalized
    last_word = changed_name.rsplit(None, 1)[-1]
    if last_word.islower():
        changed_name = re.sub(last_word, last_word.title(), changed_name)
    ##print changed_name
    return changed_name

def updating_phone(phone):
    '''
    Clean phone number
    Standard phone format (S.P.F): +1 (408)###-####
    +1 is the US Code
    (408) is the San Jose code
    The info is from this site
    https://www.timeanddate.com/worldclock/dialingcodes.html?p1=1046&p2=283&number=
    After cleaning, there are 3 situation
    '''
    '''
    uncomment the double hashed lines for debug
    '''

    ##original_phone = phone  

    # Remove +1, -, whitespaces, (), . or + from phone numbers
    phone = re.sub("\+1", "", phone)
    phone = re.sub("-", "", phone)
    phone = re.sub("[()]", "", phone)
    phone = re.sub("\s", "", phone)
    phone = re.sub("\\.", "", phone)
    phone = re.sub("\\+", "", phone)

   
    # Situation 1: Convert 10 digits number to S.P.F
    m_ten = phone_no_10.match(phone)
    if m_ten is not None:
      phone = '+1(' + phone[:3] + ')' + phone[3:6] + '-' + phone[6:10]
    # Situation 2: Convert 7 digits number to S.P.F
    m_seven = phone_no_7.match(phone)
    if m_seven is not None:
      phone = '+1(408)' + phone[1:3] + '-' + phone[3:7]
    # Situation 3: Convert 11 digits number to S.P.F
    m_eleven = phone_no_11.match(phone)
    if m_eleven is not None:
      phone = '+' + phone[:1] + '(' + phone[1:4] + ')' + phone[4:7] + '-' + phone[7:11]

    # Check all the matching requirements
    if (m_seven is not None) or (m_ten is not None) or (m_eleven is not None):
      return phone
    else:
        ##print "wrong phone number: ", original_phone
        return None

def updating_postal(p_code):
    """
    Clean postal code
    The Postal Code in San Jose have two formats
    CA {ZIP5}-{ZIP4}
    CA {ZIP5}
    We are adding CA infront of Postal Code
    i.e CA=Califonia
    """

    # Remove CA and whitespace from original postal code
    p_code = re.sub("CA", "", p_code)
    p_code = re.sub("\s", "", p_code)

    # Use regex to match postal code
    m = POSTCODE.match(p_code)
    if m is not None:
      p_code = 'CA ' + p_code
      return p_code
    else:
      #print "WRONG POSTAL CODE:", p_code
      return None

'''
remove the double hash to see the auditing .Succesive iterations were run
using this function which calls the audit_street function
after each round the mapping and expected values were added for better auditing
'''
##def mock():
    ##audit_street('san-jose_california.osm')
    ##print c
##mock()
