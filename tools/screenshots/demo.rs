const LIMIT: f64 = 0.42;

struct Reading { id: u32, value: f64 }

fn clean(raw: &[Reading]) -> Vec<f64> {
    let mut out = Vec::new();
    for r in raw {
        if r.value > LIMIT { continue; }
        out.push(r.value);
    }
    out
}
