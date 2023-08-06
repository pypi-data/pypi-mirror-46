import queue

def binary_search(arr, val, left=None, right=None, most='left'):
    '''
    [args]
        arr :
            1-d array of size n and has index 0 to n-1
            each element must support '<' and '>' operator
        val :
            the key value you are looking for
        left :
            leftmost of the search range in arr
        right :
            rightmost of the search range in arr
        most :
            choice to find leftmost value or rightmost value if there exists same values in arr
            should be one of the ['left', 'right']

    [return]
        index of the key value in array
    '''

    assert most in ['left', 'right'], "[most] should be one of the ['left', 'right']."

    size = len(arr)

    if not left:
        left = 0
    if not right:
        right = size

    assert 0 <= left < size, "[left] should be in range [0, size)"
    assert 0 <= right < size, "[right] should be in range [0, size)"
    assert left <= right, "should be [left] <= [right]"

    while True:
        if left == right:
            return left

        if most == 'left':
            mid = (left + right) // 2
        else:
            mid = (left + right + 1) // 2

        if most == 'left':
            if arr[mid] < val:
                left = mid + 1
            else:
                right = mid
        else:
            if arr[mid] > val:
                right = mid - 1
            else:
                left = mid

    return None

def dijkstra(adj, src, dest=None, inf=999999999):
    '''
    [args]
        adj :
            the list of edges of each node, i.e. the list of (dist, next_node)
            for example, adj = [(1, 5), (0, 3)] means [edge 0->1] has cost 5 and [edge 1->0] has cost 3
        src :
            the index of source(start) node of the search
        dest :
            the index of destination(end) node of the search
            if dest=None, return all distances
        inf :
            the value to represent infinity

    [return]
        if dest=None, all distances
        else, distance to dest
    '''

    dist = [inf for i in range(len(adj))]
    dist[src] = 0

    q = queue.PriorityQueue()
    q.put((0, src))
    while q.size() > 0:
        cost, here = q.get()
        if dist[here] < cost:
            continue
        for i in range(len(adj[here])):
            there = adj[here][i][0]
            next_dist = cost + adj[here][i][1]
            if dist[there] > next_dist:
                dist[there] = next_dist
                q.put((next_dist, there))

    if dest:
        return dist[dest]

    return dist

