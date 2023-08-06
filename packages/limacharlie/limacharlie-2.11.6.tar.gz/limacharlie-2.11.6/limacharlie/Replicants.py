from Sensor import Sensor

class _Replicant( object ):
    def __init__( self, manager ):
        self._manager = manager

class Responder( _Replicant ):
    def sweep( self, sid ):
        if isinstance( sid, Sensor ):
            sid = sid.sid
        self._manager.replicantRequest( 'responder', {
            'action' : 'sweep',
            'sid' : sid,
        }, False )

class Yara( _Replicant ):
    def scan( self, sid, sources ):
        if isinstance( sid, Sensor ):
            sid = sid.sid
        self._manager.replicantRequest( 'yara', {
            'action' : 'scan',
            'sid' : sid,
            'sources' : sources,
        }, False )

class Integrity( _Replicant ):
    def sweep( self, sid ):
        if isinstance( sid, Sensor ):
            sid = sid.sid
        self._manager.replicantRequest( 'integrity', {
            'action' : 'sweep',
            'sid' : sid,
        }, False )