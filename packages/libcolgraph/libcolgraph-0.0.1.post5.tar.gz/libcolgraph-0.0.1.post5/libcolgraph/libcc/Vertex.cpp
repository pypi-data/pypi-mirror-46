#ifndef __VERTEX_CPP__
#define __VERTEX_CPP__

#include "Vertex.h"

Vertex::
Vertex() {}

Vertex::
Vertex(long name_)
    : name(name_)
{}

Vertex::
~Vertex()
{}

long
Vertex::
get_name()
{
    return name;
}

void
Vertex::
add_neighbor(Vertex& other)
{
    neighbors.insert(other.get_name());
}

std::unordered_set<long>::iterator
Vertex::
get_neighbors()
{
    // TODO
}

#endif
