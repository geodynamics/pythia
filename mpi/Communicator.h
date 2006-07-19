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

#if !defined(pympi_Communicator_h__)
#define pympi_Communicator_h__

#include <mpi.h>

namespace mpi {

    class Group;
    class Communicator;
}

class mpi::Communicator {
// interface
public:
    
    int size() const {
        int size;
        return (MPI_Comm_size(_communicator, &size) == MPI_SUCCESS) ? size : -1;
    }
    
    int rank() const {
        int rank;
        return (MPI_Comm_rank(_communicator, &rank) == MPI_SUCCESS) ? rank : -1;
    }

    void barrier() const { MPI_Barrier(_communicator); }
    
    void cartesianCoordinates(int rank, int dim, int * coordinates) const {
        MPI_Cart_coords(_communicator, rank, dim, coordinates);
    }

    MPI_Comm handle() const { return _communicator; }

    // factories
    inline Communicator * communicator(const Group & group) const;
    
    Communicator * cartesian(int size, int * procs, int * periods, int reorder) const {
        MPI_Comm cartesian;
        int status = MPI_Cart_create(_communicator, size, procs, periods, reorder, &cartesian);
        if (status != MPI_SUCCESS || cartesian == MPI_COMM_NULL) {
            return 0;
        }
        return new Communicator(cartesian);
    }


// meta-methods
public:
    Communicator(MPI_Comm handle) :
        _communicator(handle) {}
    
    ~Communicator() { MPI_Comm_free(&_communicator); }

// hide these
private:
    Communicator(const Communicator &);
    Communicator & operator=(const Communicator &);

// instance atributes
protected:

    MPI_Comm _communicator;
};


#if !defined(pympi_Group_h__)
#include "Group.h"
#endif


mpi::Communicator * mpi::Communicator::communicator(const Group & group) const {
    MPI_Comm oldHandle = _communicator;
    MPI_Group groupHandle = group.handle();
    MPI_Comm comm;
    int status = MPI_Comm_create(oldHandle, groupHandle, &comm);
    if (status != MPI_SUCCESS || comm ==  MPI_COMM_NULL) {
        return 0;
    }
    return new Communicator(comm);
}


#include "_mpimodule.h"


#endif

// version
// $Id: Communicator.h,v 1.1.1.1 2005/03/08 16:13:30 aivazis Exp $

//
// End of file
