Datavore-client - Python Client library to get data 
from LOPS Datavore services
=============================================================================

Installation : 

    pip install datavoreclient

Usage example:

    >>> from datavoreclient import Datalaps
    >>> dl = Datalaps()
    >>> idxlist = dl.searchIndexes('.*smos.*argo', return_id_only=False)
    >>> dl.getTimeserie(idxlist[0][0], 'SSSSAT', '-20,-20,20,20', groupby='yyyy-MM')

