use std::collections::HashMap;

/// Readings above this value are sensor noise.
const LIMIT: f64 = 0.42;

#[derive(Debug)]
struct Reading<'a> {
    id: &'a str,
    value: f64,
}

fn clean<'a>(raw: &HashMap<&'a str, f64>) -> Vec<Reading<'a>> {
    let mut out = Vec::new();
    for (&id, &value) in raw {
        if value > LIMIT {
            continue;
        }
        out.push(Reading { id, value });
    }
    println!("kept {} readings", out.len());
    out
}
