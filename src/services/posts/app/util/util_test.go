package util

import (
 "strings"
 "testing"
)

func TestGenerateRandomIDLength(t *testing.T) {
 id := GenerateRandomID()
 expectedLength := 19
 if len(id) != expectedLength {
  t.Errorf("Expected length of generated ID to be %d, got %d", expectedLength, len(id))
 }
}

func TestGenerateRandomIDSegments(t *testing.T) {
 id := GenerateRandomID()
 segments := strings.Split(id, "-")
 expectedSegments := 4
 if len(segments) != expectedSegments {
  t.Fatalf("Expected %d segments in the generated ID, got %d", expectedSegments, len(segments))
 }
}

func TestGenerateRandomIDSegmentLengths(t *testing.T) {
 id := GenerateRandomID()
 segments := strings.Split(id, "-")
 expectedSegmentLengths := []int{4, 4, 4, 4}
 for i, segment := range segments {
  if len(segment) != expectedSegmentLengths[i] {
   t.Errorf("Expected segment %d to have length %d, got %d", i+1, expectedSegmentLengths[i], len(segment))
  }
 }
}

func TestGenerateRandomIDCharacters(t *testing.T) {
 id := GenerateRandomID()
 segments := strings.Split(id, "-")
 charset := "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
 for _, segment := range segments {
  for _, char := range segment {
   if !strings.ContainsRune(charset, char) {
    t.Errorf("Segment %s contains invalid character %c", segment, char)
   }
  }
 }
}
