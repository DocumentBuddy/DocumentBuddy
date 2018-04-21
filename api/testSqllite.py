from sqlite import Sqlite
import pprint

sqlite = Sqlite('./example.db')
sqlite.drop_table('main')
sqlite.drop_table('keywords')
sqlite.create_table_main()
sqlite.create_table_keywords()
sqlite.insert_data('link',('keyword1', 'keyword2'),'text','kfw_sth')
sqlite.insert_data('/pathToSomeWhere',('Flo','Badjosh'), 'Hallo Hallo', 'chat')
sqlite.insert_data('/pathToSomeWhereElse',('Flo2','Badjosh2'), 'Hallo2 Hallo2', 'chat2')
sqlite.insert_data('/pathToSomeWhereElse',('link', 'text'),'textblablabla', 'some categry')


# Data as array
pprint.pprint(sqlite.select_all('main'))
pprint.pprint(sqlite.select_all('keywords'))
print("*************************************************")
print(sqlite.select_all_precise_by_keyword(''))
print(sqlite.select_all_precise_by_keyword('keyword2'))
print(sqlite.select_link_precise_by_keyword('keyword1'))
pprint.pprint(sqlite.select_all_including_keyword('keyword'))
pprint.pprint(sqlite.select_link_including_keyword('keyword'))
pprint.pprint(sqlite.select_link_including_keyword('JOsh'))
pprint.pprint(sqlite.select_from_keywords(['keyword','Flo']))

#sqlite.truncateDatabase('main')
#sqlite.truncateDatabase('keywords')
# handle end of connection
sqlite.close_connection()