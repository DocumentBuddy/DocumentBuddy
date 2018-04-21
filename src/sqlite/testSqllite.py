from sqlite import Sqlite
import pprint

sqlite = Sqlite('./example.db')
sqlite.insertData('link',('keyword1', 'keyword2'),'text','kfw_sth')
sqlite.insertData('/pathToSomeWhere',('Flo','Badjosh'), 'Hallo Hallo', 'chat')
sqlite.insertData('/pathToSomeWhereElse',('Flo2','Badjosh2'), 'Hallo2 Hallo2', 'chat2')
sqlite.updateMain('/pathToSomeWhereElse',('link', 'text'),('./PathToNoReturn', 'It works'))


# Data as array
print(sqlite.selectAllPreciseByKeyword('keyword1'))
print(sqlite.selectLinkPreciseByKeyword('keyword1'))
pprint.pprint(sqlite.selectAllIncludingKeyword('keyword'))
pprint.pprint(sqlite.selectLinkIncludingKeyword('keyword'))
pprint.pprint(sqlite.selectLinkIncludingKeyword('JOsh'))
pprint.pprint(sqlite.selectAll('main'))

sqlite.truncateDatabase('main')
sqlite.truncateDatabase('keywords')
# handle end of connection
sqlite.closeConnection()