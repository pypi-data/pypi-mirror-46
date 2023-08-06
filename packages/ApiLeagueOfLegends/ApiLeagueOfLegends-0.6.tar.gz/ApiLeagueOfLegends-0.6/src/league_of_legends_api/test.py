from league_of_legends_api.Api.leaugue_api import SummonerV4, MatchV4
from league_of_legends_api.Database.database import Database
import time

db = Database()
#db.save_keys_to_database(keys)
keys = db.load_keys_in()
summoner = SummonerV4(keys)
response, key = summoner.get_summoner_by_name("SaItySurprise")
#match = MatchV4(keys)
#response = match.get_match_list_by_account_id(salty['accountId'], key.id, champion='1', season='11')
#start_time = time.time()
#match.run_pool_request(['3797884873', '3705535630', '3677411775', '3548509543', '3531522978', '3510590369',
#                        '3504114075', '4011269221', '4011200839', '4011016144', '4011269221', '4011200839',
#                        '4011016144', '4010876109', '4010278359', '4009945080', '4009912212', '4009632648',
#                        '4004794953', '4004771327', '4004341385', '4002425441', '4002399134', '4002140606',
#                        '3998068328', '3995968654', '3995788006', '3995650519', '3995511505', '3995447122',
#                        '3991913197', '3991843951', '3990582079', '3989754426', '3987943720', '3987886979',
#                        '3987785657', '3987706049', '3987488147', '3987409676', '4009416876', '4008966898',
#                        '4004393930', '4004264617', '4002052857', '4000864151', '3995300114', '3992556085',
#                        '3992509250', '3982573076', '3974626531', '3973901315', '3973723245', '3972808418',
#                        '3972796626', '3972420300', '3972395600', '3972320407', '4010870239', '4010000907'])
#end_time = time.time()
#print(f'request: {end_time-start_time}')

print(response, key)
