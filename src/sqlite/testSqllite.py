from sqlite import Sqlite
import pprint

sqlite = Sqlite('./example.db')
sqlite.insertData('link',('keyword1', 'keyword2'),'text','kfw_sth')
sqlite.insertData('/pathToSomeWhere',('Flo','Badjosh'), 'Hallo Hallo', 'chat')


# Data as array
print(sqlite.selectAllPreciseByKeyword('keyword1'))
print(sqlite.selectLinkPreciseByKeyword('keyword1'))
pprint.pprint(sqlite.selectAllIncludingKeyword('keyword'))
pprint.pprint(sqlite.selectLinkIncludingKeyword('keyword'))
pprint.pprint(sqlite.selectLinkIncludingKeyword('JOsh'))
pprint.pprint(sqlite.selectAll('main'))

# handle end of connection
sqlite.closeConnection()