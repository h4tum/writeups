
use rayon::prelude::*;
use std::collections::HashSet;
use num_bigint::BigUint;

use std::sync::{Arc, atomic::{AtomicUsize, AtomicBool, Ordering}, Mutex};
use std::thread;
use std::time::Duration;


fn record(msg: &[bool], mic: &[BigUint]) -> BigUint {
    msg.iter().zip(mic).filter(|(&msg_bit, _)| msg_bit).map(|(_, mic_val)| mic_val.clone()).sum()
}

const N : usize = 42;

struct BruteForceData {
    mic : Vec<BigUint>,
    target : BigUint,
    first_bits : usize,
    last_bits : usize,
    first_charset : Vec<u8>,
    last_charset : Vec<u8>,
    charset : Vec<u8>,
    num_chars : usize,
    

    counter : Arc<AtomicUsize>,
    found : Arc<AtomicBool>,

        
    result: Arc<Mutex<Option<Vec<bool>>>>,
}

fn map_and_remove_duplicates<F>(input: Vec<u8>, mapper: F) -> Vec<u8>
where
    F: Fn(u8) -> u8,
{
    let mut unique_values = HashSet::new();
    let mut result = Vec::new();

    for value in input {
        let mapped_value = mapper(value);
        if unique_values.insert(mapped_value) {
            result.push(mapped_value);
        }
    }

    result
}

fn bitstring_to_ascii(bitstring: Vec<bool>) -> String {
    let mut result = String::new();
    let mut byte: u8 = 0;
    let mut bit_count = 0;

    for bit in bitstring {
        byte |= (bit as u8) << (7 - bit_count);
        bit_count += 1;
        if bit_count == 8 {
            result.push(byte as char);
            byte = 0;
            bit_count = 0;
        }
    }

    result
}


fn bool_vec_to_bitstring(bool_vec: Vec<bool>) -> String {
    let mut bitstring = String::new();
    for bit in bool_vec {
        if bit {
            bitstring.push('1');
        } else {
            bitstring.push('0');
        }
    }
    bitstring
}

fn lowest_n_bits(byte: u8, n: usize) -> Vec<bool> {
    let mut bits : Vec<bool> = Vec::new();
    for i in 0..n {
        bits.push((byte & (1 << i)) != 0)
    }
    bits.reverse();
    bits
}

fn highest_n_bits(byte: u8, n: usize) -> Vec<bool> {
    let mut bits : Vec<bool> = Vec::new();
    for i in 0..n {
        bits.push((byte & (1 << (7 - i))) != 0)
    }
    bits
}


fn try_characters(data : &BruteForceData, i : usize) -> bool {
    let mut index = i;

    let mut msg_chunk : Vec<bool> = Vec::new();

    let mut char = data.first_charset[index % data.first_charset.len()];
    index /= data.first_charset.len();

    msg_chunk.extend(lowest_n_bits(char, data.first_bits));
    
    for _j in (0..data.num_chars).rev() {
        char = data.charset[index % data.charset.len()];
        msg_chunk.extend(highest_n_bits(char, 8));
        index /= data.charset.len();
    }

    let char = data.last_charset[index % data.last_charset.len()];

    msg_chunk.extend(lowest_n_bits(char, data.last_bits));


    if msg_chunk.len() < N {
        println!("WRONG CHUNKSIZE: {}, {}, {}, {}", msg_chunk.len(), data.first_bits, data.num_chars, data.last_bits);
    }

    let c = record(&msg_chunk, &data.mic);
    if c == data.target {
        println!("{}", bool_vec_to_bitstring(msg_chunk.clone()));
        data.found.store(true, Ordering::Relaxed);
        *data.result.lock().unwrap() = Some(msg_chunk);
        return true;
    }
    
    // Increment the counter
    data.counter.fetch_add(1, Ordering::Relaxed);
    return false;
}

fn main() {
    //let mut rng = rand::thread_rng();
    //let ((ps, t, m), mic) = compose(n, &mut rng);

    /* Atual mic */
    let raw_mic = [26164716679782610683071400 as u128, 18179536354421749943360181 as u128, 5665675605611009327234952 as u128, 50306696368015064022136043 as u128, 9760129112235435790997053 as u128, 55666059844053563833206217 as u128, 16844592035444290437017126 as u128, 38380596544512184351649759 as u128, 8422829610606521010459307 as u128, 61991593557938451876941660 as u128, 39790447025261860761497646 as u128, 48017326044343373440883482 as u128, 56020453465553890215405886 as u128, 33717630577181456697432100 as u128, 38446470352430301120764167 as u128, 11956286975976159307849939 as u128, 47803055605410068453065938 as u128, 45915004803511711931436810 as u128, 24482601816186282662870243 as u128, 25803830771195376281772430 as u128, 35407508732033692038517544 as u128, 61180319487483561607584508 as u128, 25231125861794574504466017 as u128, 8313835456593256084156278 as u128, 17127389362891025344120144 as u128, 21245871665329880303420019 as u128, 38878412244851399679662521 as u128, 38873829041129616412914108 as u128, 55803139319518810427462325 as u128, 4480398056669715718609757 as u128, 16723813500382973499318355 as u128, 46788850793793785768241956 as u128, 18363270968918184887203944 as u128, 2919614635435884742895127 as u128, 38003982387728441304493811 as u128, 5066781076320234588607777 as u128, 2160276302660722051676110 as u128, 47965211574081273776856665 as u128, 14735899017054553490198493 as u128, 14455868058721210953072395 as u128, 59777806226033755809142580 as u128, 43667948754413413362501037 as u128];

    /* Fake mic */
    //let raw_mic = [33971045157188907704839994 as u128, 18664410019279741480431157, 26356111145275097474387108, 17301056165995554536751827, 38286158725585092332397810, 54505526844104964138410856, 26326778926361029783930284, 26852248432018659579316098, 2116268396330742195986907, 39120060877880394909358187, 29797655245009771599895746, 10213326016824940893222659, 46547481020285408873571365, 29154809541998917058455407, 13687247666721543275102630, 56004223080729776766705862, 29298755833062216547687019, 5647406329950951555315836, 58630793244226572726365618, 42451818839425462076538059, 38341084110815955062733353, 49801900466273053847870894, 5334224015400079453349364, 28382610360029524590545635, 25600746456997002423668267, 5198087001221560218170924, 28824991128877179763244097, 38492689433522933949833328, 1499677341948430706572487, 46578515405030817721928778, 5769085232083106836834921, 61057359324107398599479798, 7767536867917327779301785, 19772343421484846988703234, 36951514173586074311729975, 51562732194382537744636258, 51093954956070910028830908, 28747850301156306504818349, 20135465774493366776954888, 47864018546601706787457789, 22388625077968412975828656, 41695481675085613214621086 as u128];

    let mic : Vec<BigUint> = raw_mic.iter().map(|&m| BigUint::from(m)).collect();

    /* Actual output */
    let raw_output = [ 591191755265294600006904240 as u128, 612990134375087714919032704 as u128, 702014866447865251118799888 as u128, 631408587334297368272903359 as u128, 531069814353289175343659237 as u128, 619506025951321329935979611 as u128, 633106357798876645310170585 as u128, 762239129094955827352040826 as u128, 645540547612149444739609749 as u128, 155982684851883997809008793 as u128];

    /* Fake output */
    //let raw_output = [488609905188431140811203258 as u128, 751704351738603433262987580 as u128, 586114897302466198691466657 as u128, 255027285148414344465436213 as u128];

    let output : Vec<BigUint> = raw_output.iter().map(|&m| BigUint::from(m)).collect();

    

    // stop thread
    println!("{:?}", mic);


    //let charset : Vec<u8> = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789{}_ ".chars().map(|x| x as u8).collect();
    let mut charset: Vec<u8> = (32..127).map(|c| c as u8).collect();
    charset.push(0);
    let num_chars = charset.len();
    let total_combinations = num_chars.pow(5) * 2 as usize;

    

    println!("{}", total_combinations);



    let mut cur_bits = 0;

    let mut result : Vec<bool> = Vec::new();

    let num_outputs = output.len();

    for (i, target) in output.into_iter().enumerate() {
        // Atomic counter for progress tracking
        let counter = Arc::new(AtomicUsize::new(0));
        let counter_clone = Arc::clone(&counter);
        
        
        let found = Arc::new(AtomicBool::new(false));
        let found_clone = Arc::clone(&found);

        let first_bits = 8 - (cur_bits % 8);
        cur_bits += N;

        let last_bits;

        if (N - first_bits) % 8 == 0 {
            last_bits = 8;
        }
        else {
            last_bits = (N - first_bits) % 8;
        }


        let num_chars = (N - first_bits - last_bits) / 8;

        println!("first_bits: {}, last_bits: {}, num_chars: {}\n", first_bits, last_bits, num_chars);

        let first_charset = map_and_remove_duplicates(charset.clone(), |x| (x as u16 % (2 as u16).pow(first_bits as u32)) as u8);
        let last_charset = map_and_remove_duplicates(charset.clone(), |x| (x >> (8 - last_bits)));

        println!("{}|{}", first_charset.len(), last_charset.len());

        let total_combinations = first_charset.len() * last_charset.len() * charset.len().pow(num_chars as u32);

        let data = BruteForceData{
            mic: mic.clone(), 
            target: target, 
            first_bits: first_bits, 
            last_bits: last_bits,
            first_charset: first_charset,
            last_charset: last_charset,
            charset: charset.clone(),
            num_chars : num_chars,
            counter : counter,
            found : found,
            result : Arc::new(Mutex::new(None)),
        };

        // Spawn a thread to periodically print the progress
        thread::spawn(move || {
            loop {
                let count = counter_clone.load(Ordering::Relaxed);
                if found_clone.load(Ordering::Relaxed) || count == total_combinations {
                    break;
                }
                println!("At block {:2}/{}", i+1, num_outputs);
                println!("Total:    {}", total_combinations);
                println!("Processed {} combinations so far...", count);
                thread::sleep(Duration::from_secs(1));
            }
        });

        let _r = (0..total_combinations).into_par_iter().find_any(|&i| {
            try_characters(&data, i)
        });

        if let Some(_r) = data.result.lock().unwrap().clone() {
            println!("Found {}", bool_vec_to_bitstring(_r.clone()));
            result.extend(_r);
        } else {
            println!("None found!");
            break;
        }
        ;
    }
    println!("Found {}", bitstring_to_ascii(result));
}

