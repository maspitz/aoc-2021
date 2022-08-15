package main

// day18.go solves Advent of Code 2021, day 18
// It expects the input data as a file named 'input.txt'

import (
	"fmt"
	"strings"
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


func add(s1 string, s2 string) string {
	return "[" + s1 + "," + s2 + "]"
}

func split(s string) string {
	digits := 0
	startnum := 0
	stopnum := 0
	for i, c := range(s) {
		if c == '[' || c == ']' || c == ',' {
			if digits > 1 {
				startnum = i - digits
				stopnum = i
				break
			}
			digits = 0
		} else {
			digits += 1
		}
	}
	if startnum == 0 {
		return ""
	}
	number, err := strconv.Atoi(s[startnum:stopnum])
	if err != nil {
		log.Fatal(err)
	}
	leftval := number / 2
	rightval := number / 2 + number % 2
	return s[:startnum] + "[" + strconv.Itoa(leftval) + "," + strconv.Itoa(rightval) + "]" + s[stopnum:]
}

func explode(s string) string {
	depth := 0
	left_bracket := 0
	for i, c := range(s) {
		if c == '[' {
			if depth == 5 {
				left_bracket = i
				break
			}
			depth += 1
		} else if c == ']' {
			depth -= 1
		}
	}
	if left_bracket == 0 {
		return ""
	}
	comma := strings.IndexByte(s[left_bracket:], ',') + left_bracket
	if comma == -1 {
		log.Fatal("Bad format: comma missing")
	}
	right_bracket := strings.IndexByte(s[comma:], ']') + comma
	if right_bracket == -1 {
		log.Fatal("Bad format: right bracket missing")
	}
	leftval, err := strconv.Atoi(s[left_bracket+1:comma])
	if err != nil {
		log.Fatal(err)
	}
	rightval, err := strconv.Atoi(s[comma+1:right_bracket])
	if err != nil {
		log.Fatal(err)
	}
	_ = leftval
	_ = rightval
	return "FOO"
}
	



func main() {
	file, err := os.Open("input.txt")
	if err != nil {
		log.Fatal(err)
	}
	scanner := bufio.NewScanner(file)
	scanner.Split(bufio.ScanLines)
	var snailfish []string
	for scanner.Scan() {
		snailfish = append(snailfish,scanner.Text())
	}
	file.Close()
	for _, s := range(snailfish) {
		fmt.Println(split(s))
	}
}
