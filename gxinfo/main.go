package main

import (
	"bufio"
	"fmt"
	"os"
	"sort"
	"strconv"
	"strings"
)

type GCodeSetting struct {
	Line      int
	Command   string
	Parameter string
	Value     float64
}

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Usage: gxinfo <file.gx>")
		return
	}

	filePath := os.Args[1]
	settings := parseGXFile(filePath)

	sort.Slice(settings, func(i, j int) bool {
		return settings[i].Line < settings[j].Line
	})

	for _, s := range settings {
		fmt.Printf("Line %d: %s %s = %.2f\n", s.Line, s.Command, s.Parameter, s.Value)
	}
}

func parseGXFile(filePath string) []GCodeSetting {
	file, err := os.Open(filePath)
	if err != nil {
		fmt.Println("Error opening file:", err)
		return nil
	}
	defer file.Close()

	var settings []GCodeSetting
	scanner := bufio.NewScanner(file)
	lineNumber := 0

	for scanner.Scan() {
		line := scanner.Text()
		lineNumber++

		if strings.HasPrefix(line, "M104") || strings.HasPrefix(line, "M140") || strings.HasPrefix(line, "M109") || strings.HasPrefix(line, "M190") || strings.HasPrefix(line, "M106") || strings.HasPrefix(line, "M107") {
			parts := strings.Fields(line)
			if len(parts) > 1 {
				command := parts[0]
				for _, part := range parts[1:] {
					if strings.HasPrefix(part, "S") {
						value, err := strconv.ParseFloat(part[1:], 64)
						if err == nil {
							settings = append(settings, GCodeSetting{
								Line:      lineNumber,
								Command:   command,
								Parameter: "S",
								Value:     value,
							})
						}
					}
				}
			}
		}
	}

	if err := scanner.Err(); err != nil {
		fmt.Println("Error reading file:", err)
	}
	return settings
}
