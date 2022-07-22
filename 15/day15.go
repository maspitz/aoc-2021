package main

// day15.go solves Advent of Code 2021, day 15
// On my computer it runs about 40x faster than my day15.py.
// It expects the input data as a file named 'input.txt'

import (
	"container/heap"
	"fmt"
	"strings"
	"io/ioutil"
	"log"
)

// Node represents a node's entry in the priority queue used by Dijkstra.
type Node struct {
	cost int // the cost to the node when enqueued
	idx  int // the node's index in the Grid
}

// A NodeHeap implements heap.Interface and holds Nodes.
type NodeHeap []Node

func (nq NodeHeap) Len() int           { return len(nq) }
func (nq NodeHeap) Less(i, j int) bool { return nq[i].cost < nq[j].cost }
func (nq NodeHeap) Swap(i, j int)      { nq[i], nq[j] = nq[j], nq[i] }

func (nq *NodeHeap) Push(x interface{}) {
	*nq = append(*nq, x.(Node))
}

func (nq *NodeHeap) Pop() interface{} {
	old := *nq
	n := len(old)
	popped := old[n-1]
	*nq = old[0 : n-1]
	return popped
}

// The Grid is a graph generated from a 2d array of digits
// as described in the 2021 day 15 problem.
type Grid struct {
	weights    []int // the weights of edges going to a given node
	rows, cols int   // invariant: rows * cols equals len(weights)
	max_cost   int   // an upper bound on the maximum path cost
}

// Neighbors returns a slice of the nodes that neighbor the given node.
func (g Grid) Neighbors(from_node int) []int {
	to_nodes := make([]int, 0, 4)
	row := from_node / g.cols
	col := from_node % g.cols
	if row > 0 {
		to_nodes = append(to_nodes, from_node-g.cols)
	}
	if col > 0 {
		to_nodes = append(to_nodes, from_node-1)
	}
	if col < g.cols-1 {
		to_nodes = append(to_nodes, from_node+1)
	}
	if row < g.rows-1 {
		to_nodes = append(to_nodes, from_node+g.cols)
	}
	return to_nodes
}

func MakeGrid(s string) Grid {
	lines := strings.Split(s, "\n")
	rows := len(lines)
	cols := len(lines[0])
	weights := make([]int, rows*cols)
	for row, line := range lines {
		if len(line) == 0 {
			continue
		}
		for col, digit := range []byte(line) {
			weights[col+row*cols] = int(digit - '0')
		}
	}
	return Grid{
		weights:  weights,
		rows:     rows,
		cols:     cols,
		max_cost: (rows + cols) * 10,
	}
}

func PrintGrid(g Grid) {
	for i := 0; i < g.rows; i++ {
		fmt.Println(g.weights[i*g.cols : (i+1)*g.cols])
	}
}

func MakeBigGrid(g Grid) Grid {
	rows := g.rows * 5
	cols := g.cols * 5
	weights := make([]int, len(g.weights) * 25)
	for i := 0; i < rows; i++ {
		g_i := i % g.rows
		for j := 0; j < cols; j++ {
			g_j := j % g.cols
			increment := i / g.rows + j / g.cols
			inc_weight := g.weights[g_i * g.cols + g_j] + increment
			weights[i * cols + j] = (inc_weight - 1) % 9 + 1
		}
	}
	return Grid{
		weights: weights,
		rows: rows,
		cols: cols,
		max_cost: (rows + cols) * 10,
	}
}


// Find the cost of the least path from nodes 0 to n-1.
func LeastPathCost(g Grid) int {
	n_nodes := len(g.weights)
	nq := &NodeHeap{Node{cost: 0, idx: 0}}
	heap.Init(nq)

	best_costs := make([]int, n_nodes)
	for i := range best_costs {
		best_costs[i] = g.max_cost
	}
	best_costs[0] = 0

	visited := make([]bool, n_nodes)
	for nq.Len() > 0 {
		node := heap.Pop(nq).(Node)
		if visited[node.idx] {
			continue
		}
		for _, to_idx := range g.Neighbors(node.idx) {
			if visited[to_idx] {
				continue
			}
			trial_cost := node.cost + g.weights[to_idx]
			if trial_cost < best_costs[to_idx] {
				best_costs[to_idx] = trial_cost
				heap.Push(nq, Node{cost: trial_cost,
					idx: to_idx})
			}
		}
		visited[node.idx] = true
	}
	return best_costs[n_nodes - 1]
}

func main() {
	content, err := ioutil.ReadFile("input.txt")
	if err != nil {
		log.Fatal(err)
	}
	s := string(content)
	grid := MakeGrid(strings.TrimSpace(s))
	big_grid := MakeBigGrid(grid)
	fmt.Println(LeastPathCost(grid))
	fmt.Println(LeastPathCost(big_grid))
}
