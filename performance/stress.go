package main

import (
	"bytes"
	"encoding/json"
	"flag"
	"fmt"
	"net/http"
	"sync"
	"time"
)

type Dialog struct {
	Role    string `json:"role"`
	Content string `json:"content"`
}

type DialogRequest struct {
	Dialogs      [][]Dialog `json:"dialogs"`
	Temperature  float64    `json:"temperature"`
	TopP         float64    `json:"top_p"`
	MaxSeqLen    int        `json:"max_seq_len"`
	MaxBatchSize int        `json:"max_batch_size"`
	MaxGenLen    *int       `json:"max_gen_len,omitempty"`
}

func sendRequest(wg *sync.WaitGroup, client *http.Client, url string, request DialogRequest) {
	defer wg.Done()

	reqBody, err := json.Marshal(request)
	if err != nil {
		fmt.Printf("Error marshalling request: %v\n", err)
		return
	}

	resp, err := client.Post(url, "application/json", bytes.NewBuffer(reqBody))
	if err != nil {
		fmt.Printf("Error sending request: %v\n", err)
		return
	}
	defer resp.Body.Close()

	if resp.StatusCode == http.StatusOK {
		var responseData map[string]interface{}
		if err := json.NewDecoder(resp.Body).Decode(&responseData); err != nil {
			fmt.Printf("Error decoding response: %v\n", err)
			return
		}
		results := responseData["results"].([]interface{})
		for _, result := range results {
			fmt.Printf("> %v\n", result)
		}
	} else {
		fmt.Printf("Error: %v\n", resp.Status)
	}
}

func main() {
	var numClients int
	var temperature float64
	var topP float64
	var maxSeqLen int
	var maxBatchSize int
	var maxGenLen int

	flag.IntVar(&numClients, "num_clients", 10, "Number of concurrent clients")
	flag.Float64Var(&temperature, "temperature", 0.6, "Temperature")
	flag.Float64Var(&topP, "top_p", 0.9, "Top P")
	flag.IntVar(&maxSeqLen, "max_seq_len", 512, "Max sequence length")
	flag.IntVar(&maxBatchSize, "max_batch_size", 4, "Max batch size")
	flag.IntVar(&maxGenLen, "max_gen_len", 0, "Max generation length (0 for none)")
	flag.Parse()

	dialogs := [][]Dialog{
		{
			{Role: "user", Content: "what is the result of 5+3+3+3+3. Only return result."},
		},
	}

	var maxGenLenPtr *int
	if maxGenLen > 0 {
		maxGenLenPtr = &maxGenLen
	}

	request := DialogRequest{
		Dialogs:      dialogs,
		Temperature:  temperature,
		TopP:         topP,
		MaxSeqLen:    maxSeqLen,
		MaxBatchSize: maxBatchSize,
		MaxGenLen:    maxGenLenPtr,
	}

	client := &http.Client{}
	url := "http://localhost:8000/chat"

	startTime := time.Now()

	var wg sync.WaitGroup
	for i := 0; i < numClients; i++ {
		wg.Add(1)
		go sendRequest(&wg, client, url, request)
	}
	wg.Wait()

	endTime := time.Now()
	elapsedTime := endTime.Sub(startTime)
	fmt.Printf("Stress test completed in %.2f seconds\n", elapsedTime.Seconds())
}
