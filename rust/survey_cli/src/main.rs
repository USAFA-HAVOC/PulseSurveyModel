extern crate sentiment;

use std::io;

fn score_close_ended(response: &str, question_num: usize) -> i32 {
    let scoring = [
        ("strongly disagree", 1),
        ("disagree", 2),
        ("neutral", 3),
        ("agree", 4),
        ("strongly agree", 5),
    ];

    let reverse_scoring = [
        ("strongly disagree", 5),
        ("disagree", 4),
        ("neutral", 3),
        ("agree", 2),
        ("strongly agree", 1),
    ];

    if question_num == 1 || question_num == 2 {
        for &(k, v) in &reverse_scoring {
            if k == response {
                return v;
            }
        }
    } else {
        for &(k, v) in &scoring {
            if k == response {
                return v;
            }
        }
    }

    0
}

fn score_open_ended(response: &str) -> i32 {
    let analysis = sentiment::analyze(response);
    if analysis.score > 2 {
        5
    } else if analysis.score < -2 {
        1
    } else {
        3
    }
}

fn main() {
    let mut close_ended = Vec::new();
    let mut open_ended = Vec::new();

    for i in 1..=8 {
        let mut input = String::new();
        println!("Close-ended Question {}: ", i);
        io::stdin().read_line(&mut input).unwrap();
        let score = score_close_ended(&input.trim(), i);
        close_ended.push((input.trim().to_string(), score));
    }

    for i in 1..=6 {
        let mut input = String::new();
        println!("Open-ended Question {}: ", i);
        io::stdin().read_line(&mut input).unwrap();
        let score = score_open_ended(&input.trim());
        open_ended.push((input.trim().to_string(), score));
    }

    // Display results (you can format and display as required)
    println!("{:?}", close_ended);
    println!("{:?}", open_ended);
}
