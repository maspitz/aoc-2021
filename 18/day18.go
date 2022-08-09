package main

// day18.go solves Advent of Code 2021, day 18
// It expects the input data as a file named 'input.txt'

import (
	"fmt"
	//	"strings"
	"strconv"
	"bufio"
	"os"
	"log"
)


func magnitude(s string) int {
	val, err := strconv.Atoi(s)
	if err == nil {
		return val
	}
	depth := 0
	for i, c := range(s) {
		if c == '[' {
			depth += 1
		} else if c == ']' {
			depth -= 1
		} else if c == ',' && depth == 1 {
			return 3*magnitude(s[1:i]) +
				2*magnitude(s[i+1:len(s)-1])
		}
	}
	log.Fatal("magnitude failed for snailfish: ", s)
	return -1
}



func main() {
	file, err := os.Open("input.txt")
	if err != nil {
		log.Fatal(err)
	}
	scanner := bufio.NewScanner(file)
	scanner.Split(bufio.ScanLines)
	var snailfish string
	for scanner.Scan() {
		snailfish = scanner.Text()
		fmt.Println(snailfish)
		fmt.Println(magnitude(snailfish))
	}
}
