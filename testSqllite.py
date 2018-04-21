import pprint

from api.sqlite import Sqlite

sqlite = Sqlite('./api/example.db')
sqlite.drop_table('main')
sqlite.drop_table('keywords')
sqlite.drop_table('names')
sqlite.create_table_main()
sqlite.create_table_keywords()
sqlite.create_table_names()
sqlite.insert_data('link',('keyword1', 'keyword2'),'text','kfw_sth', 'toc', 'AuthorA', ('NameA', 'NameB',), 4, '2018-10-12')
sqlite.insert_data('/pathToSomeWhere',('Flo','Badjosh'), 'Hallo Hallo', 'chat', 'toc', 'AuthorA','', 4, '2018-10-12')
sqlite.insert_data('/pathToSomeWhereElse',('Flo2','Badjosh2'), 'Hallo2 Hallo2', 'chat2', 'toc', 'AuthorA', ('NameC',), 4, '2018-10-12')
sqlite.insert_data('/pathToSomeWhereElse',('link', 'text'),'textblablabla', 'some categry', 'toc', 'AuthorA', ('Paul',), 4, '2018-10-12')
sqlite.insert_data_in_keywords('3',('test',))

# Data as array
print("*************************************************")
pprint.pprint(sqlite.select_all('main'))
pprint.pprint(sqlite.select_all('keywords'))
pprint.pprint(sqlite.select_all('names'))
print("*************************************************")
print(sqlite.select_all_precise_by_keyword(''))
print(sqlite.select_all_precise_by_keyword('keyword2'))
print(sqlite.select_link_precise_by_keyword('keyword1'))
pprint.pprint(sqlite.select_all_including_keyword('Flo'))
pprint.pprint(sqlite.select_link_including_keyword('Flo'))
pprint.pprint(sqlite.select_link_including_keyword('JOsh'))
pprint.pprint(sqlite.select_from_keywords(['keyword','Flo']))

#sqlite.truncateDatabase('main')
#sqlite.truncateDatabase('keywords')
# handle end of connection
sqlite.close_connection()