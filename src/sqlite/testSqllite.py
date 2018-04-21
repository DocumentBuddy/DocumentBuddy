from sqlite import Sqlite
import pprint

sqlite = Sqlite('./example.db')
sqlite.insert_data('link',('keyword1', 'keyword2'),'text','kfw_sth')
sqlite.insert_data('/pathToSomeWhere',('Flo','Badjosh'), 'Hallo Hallo', 'chat')
sqlite.insert_data('/pathToSomeWhereElse',('Flo2','Badjosh2'), 'Hallo2 Hallo2', 'chat2')
sqlite.update_main('/pathToSomeWhereElse',('link', 'text'),('./PathToNoReturn', 'It works'))


# Data as array
print(sqlite.select_all_precise_by_keyword('keyword1'))
print(sqlite.select_link_precise_by_keyword('keyword1'))
pprint.pprint(sqlite.select_all_including_keyword('keyword'))
pprint.pprint(sqlite.select_link_including_keyword('keyword'))
pprint.pprint(sqlite.select_link_including_keyword('JOsh'))
pprint.pprint(sqlite.select_all('main'))

sqlite.truncate_database('main')
sqlite.truncate_database('keywords')
# handle end of connection
sqlite.close_connection()