// -*- C++ -*-
//
//  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//
//                              Michael A.G. Aivazis
//                        California Institute of Technology
//                        (C) 1998-2005 All Rights Reserved
//
// <LicenseText>
//
//  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//

#if !defined(pympi_Group_h__)
#define pympi_Group_h__

#include <mpi.h>

namespace mpi {

    class Group;
    class Communicator;
}


class mpi::Group {

// interface
public:
    
    int size() const {
        int size;
        return (MPI_Group_size(_group, &size) == MPI_SUCCESS) ? size : -1;
    }
    
    int rank() const {
        int rank;
        return (MPI_Group_rank(_group, &rank) == MPI_SUCCESS) ? rank : -1;
    }
    
    MPI_Group handle() const { return _group; }

    // factories
    static inline Group * group(const Communicator & comm);

    Group * include(int size, int ranks[]) const {
        MPI_Group newGroup = MPI_GROUP_NULL;
        int status = MPI_Group_incl(_group, size, ranks, &newGroup);
        if (status != MPI_SUCCESS || newGroup == MPI_GROUP_NULL) {
            return 0;
        }
        return new Group(newGroup);
    }
    
    Group * exclude(int size, int ranks[]) const {
        MPI_Group newGroup = MPI_GROUP_NULL;
        int status = MPI_Group_excl(_group, size, ranks, &newGroup);
        if (status != MPI_SUCCESS || newGroup == MPI_GROUP_NULL) {
            return 0;
        }
        return new Group(newGroup);
    }
    
// meta-methods
public:
    Group(MPI_Group handle) : _group(handle) {}
    ~Group() { MPI_Group_free(&_group); }

// hide these
private:
        
    Group(const Group &);
    Group & operator=(const Group &);

// data
protected:

    MPI_Group _group;
};


#if !defined(pympi_Communicator_h__)
#include "Communicator.h"
#endif


mpi::Group * mpi::Group::group(const mpi::Communicator & comm) {
    MPI_Comm commHandle = comm.handle();
    MPI_Group group;
    int status = MPI_Comm_group(commHandle, &group);
    if (status != MPI_SUCCESS || group == MPI_GROUP_NULL) {
        return 0;
    }
    return new Group(group);
}


#include "_mpimodule.h"


// version
// $Id: Group.h,v 1.1.1.1 2005/03/08 16:13:30 aivazis Exp $

#endif

//
// End of file
