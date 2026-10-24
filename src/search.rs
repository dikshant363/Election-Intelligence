// Election Intelligence Platform - BM25 Full-Text Search Engine
// High-performance, transliteration-aware in-process ranker

use crate::domain::SearchHit;
use std::collections::HashMap;

#[derive(Clone, Debug)]
pub struct SearchDocument {
    pub id: String,
    pub title: String,
    pub category: String,
    pub content: String,
}

pub struct BM25Index {
    docs: Vec<SearchDocument>,
    doc_lengths: Vec<usize>,
    avg_doc_length: f64,
    // term -> doc_index -> count
    inverted_index: HashMap<String, HashMap<usize, usize>>,
    // term -> number of docs containing term
    doc_frequencies: HashMap<String, usize>,
    k1: f64,
    b: f64,
}

impl BM25Index {
    pub fn new() -> Self {
        Self {
            docs: Vec::new(),
            doc_lengths: Vec::new(),
            avg_doc_length: 0.0,
            inverted_index: HashMap::new(),
            doc_frequencies: HashMap::new(),
            k1: 1.2,
            b: 0.75,
        }
    }

    pub fn build(documents: Vec<SearchDocument>) -> Self {
        let mut index = Self::new();
        let total_docs = documents.len();
        if total_docs == 0 {
            return index;
        }

        let mut total_length = 0;
        index.docs = documents;

        for (doc_idx, doc) in index.docs.iter().enumerate() {
            let tokens = tokenize(&format!("{} {}", doc.title, doc.content));
            let length = tokens.len();
            total_length += length;
            index.doc_lengths.push(length);

            let mut term_counts: HashMap<String, usize> = HashMap::new();
            for token in tokens {
                *term_counts.entry(token).or_insert(0) += 1;
            }

            for (term, count) in term_counts {
                index
                    .inverted_index
                    .entry(term.clone())
                    .or_default()
                    .insert(doc_idx, count);
                *index.doc_frequencies.entry(term).or_insert(0) += 1;
            }
        }

        index.avg_doc_length = total_length as f64 / total_docs as f64;
        index
    }

    pub fn search(&self, query: &str, limit: usize) -> Vec<SearchHit> {
        let query_terms = tokenize(query);
        if query_terms.is_empty() || self.docs.is_empty() {
            return Vec::new();
        }

        let total_docs = self.docs.len() as f64;
        let mut scores: HashMap<usize, f64> = HashMap::new();

        for term in &query_terms {
            if let Some(postings) = self.inverted_index.get(term) {
                let df = *self.doc_frequencies.get(term).unwrap_or(&0) as f64;
                // Robertson-Spärck Jones IDF
                let idf = ((total_docs - df + 0.5) / (df + 0.5) + 1.0).ln();

                for (&doc_idx, &tf) in postings {
                    let doc_len = self.doc_lengths[doc_idx] as f64;
                    let tf = tf as f64;
                    let numerator = tf * (self.k1 + 1.0);
                    let denominator =
                        tf + self.k1 * (1.0 - self.b + self.b * (doc_len / self.avg_doc_length));
                    let term_score = idf * (numerator / denominator);

                    *scores.entry(doc_idx).or_insert(0.0) += term_score;
                }
            }
        }

        let mut hit_list: Vec<(usize, f64)> = scores.into_iter().collect();
        hit_list.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap_or(std::cmp::Ordering::Equal));

        hit_list
            .into_iter()
            .take(limit)
            .map(|(idx, score)| {
                let doc = &self.docs[idx];
                SearchHit {
                    id: doc.id.clone(),
                    title: doc.title.clone(),
                    category: doc.category.clone(),
                    description: doc.content.clone(),
                    score: (score * 100.0).round() / 100.0,
                }
            })
            .collect()
    }
}

pub fn tokenize(text: &str) -> Vec<String> {
    text.to_lowercase()
        .chars()
        .map(|c| if c.is_alphanumeric() { c } else { ' ' })
        .collect::<String>()
        .split_whitespace()
        .map(|s| s.to_string())
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_bm25_search_scoring() {
        let docs = vec![
            SearchDocument {
                id: "elec-1".into(),
                title: "General Election 2026 Lok Sabha".into(),
                category: "election".into(),
                content: "National parliamentary elections across all 543 constituencies.".into(),
            },
            SearchDocument {
                id: "cand-1".into(),
                title: "Narendra Modi".into(),
                category: "candidate".into(),
                content: "Bharatiya Janata Party candidate contesting from Varanasi Uttar Pradesh."
                    .into(),
            },
            SearchDocument {
                id: "const-1".into(),
                title: "Varanasi".into(),
                category: "constituency".into(),
                content: "Parliamentary constituency code UP-77 in Uttar Pradesh.".into(),
            },
        ];

        let index = BM25Index::build(docs);
        let results = index.search("Varanasi Modi", 5);

        assert!(!results.is_empty());
        assert_eq!(results[0].category, "candidate");
        assert_eq!(results[0].id, "cand-1");
    }
}
