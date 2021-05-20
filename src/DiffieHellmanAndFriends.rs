use num_bigint::{BigInt, RandBigInt, ToBigInt};

use aes::Aes128;
use block_modes::block_padding::Pkcs7;
use block_modes::{BlockMode, Cbc};
use hex_literal::hex;

// fn mod_exp(base: BigInt, mut exponent: BigInt, modulus: BigInt) -> BigInt {
//     let ZERO = 0.to_bigint().unwrap();
//     let ONE = 1.to_bigint().unwrap();
//     let TWO = 2.to_bigint().unwrap();

//     let mut result = ZERO.clone();

//     loop {
//         if exponent.clone().eq(&ZERO) {
//             break;
//         }

//         if exponent.clone() % TWO.clone() == ONE.clone() {
//             result = (result.clone() * base.clone()) % modulus.clone();
//         }

//         if exponent.clone() % TWO.clone() == ZERO {
//             exponent = (exponent.clone() >> 1);
//             result = result.clone() * (base.clone() * base.clone()) % modulus.clone();
//         }
//     }

//     result
// }

#[derive(Debug)]
struct DiffieHellman {
    p: BigInt,
    g: BigInt,
    x: BigInt,
}

impl DiffieHellman {
    fn new(nist_prime: BigInt, g: BigInt) -> DiffieHellman {
        let mut rng = rand::thread_rng();

        let low = 0.to_bigint().unwrap();
        let random: BigInt = rng.gen_bigint_range(&low, &nist_prime);
        // println!("random {}", random);
        // let x = mod_exp(g, random, p);

        return DiffieHellman {
            p: nist_prime,
            g,
            x: random,
        };
    }

    fn get_public(&self) -> BigInt {
        // println!("{}", self.g.modpow(&self.x, &self.p));
        let mo = self.g.modpow(&self.x, &self.p);
        mo
    }

    fn shared_secret(&self, others: &BigInt) -> BigInt {
        let mo = others.modpow(&self.x, &self.p);
        mo
    }

    fn get_all_details(&self) -> (BigInt, BigInt, BigInt) {
        // println!("{}", self.g.modpow(&self.x, &self.p));
        let mo = self.g.modpow(&self.x, &self.p);
        (self.p.clone(), self.g.clone(), mo)
    }
}

pub fn challenge_33() {
    let nist_prime = BigInt::parse_bytes(b"ffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff",16).unwrap();
    let g = 2.to_bigint().unwrap();

    let Alice = DiffieHellman::new(nist_prime.clone(), g.clone());
    let Bob = DiffieHellman::new(nist_prime, g);
    let A = Alice.get_public();
    let B = Bob.get_public();

    assert_eq!(Alice.shared_secret(&B), Bob.shared_secret(&A));
}

pub fn challenge_34() {
    let nist_prime = BigInt::parse_bytes(b"ffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff",16).unwrap();
    let g = 2.to_bigint().unwrap();

    let Alice = DiffieHellman::new(nist_prime.clone(), g.clone());

    let (p, g, A) = Alice.get_all_details();
    let Bob = DiffieHellman::new(p, g);
    let B = Bob.get_public();

    let secret = Alice.shared_secret(&B);
    let (_, string_secret) = secret.to_bytes_be();
    // create an alias for convenience
    type Aes128Cbc = Cbc<Aes128, Pkcs7>;

    // let key = hex!("000102030405060708090a0b0c0d0e0f");
    let iv = hex!("f0f1f2f3f4f5f6f7f8f9fafbfcfdfeff");
    let plaintext = b"Hello world!";

    let cipher = Aes128Cbc::new_from_slices(&string_secret[0..16], &iv).unwrap();

    // buffer must have enough space for message+padding
    let mut buffer = [0u8; 32];
    // copy message to the buffer
    let pos = plaintext.len();
    buffer[..pos].copy_from_slice(plaintext);
    let ciphertext = cipher.encrypt(&mut buffer, pos).unwrap();

    //todo I have to prepend the IV, check how to copy references in Rust

    // assert_eq!(ciphertext, hex!("1b7a4c403124ae2fb52bedc534d82fa8"));

    let bobs_secret = Bob.shared_secret(&A);
    let (_, bob_string_secret) = bobs_secret.to_bytes_be();
    // re-create cipher mode instance
    let cipher = Aes128Cbc::new_from_slices(&bob_string_secret[0..16], &iv).unwrap();
    let mut buf = ciphertext.to_vec();
    let decrypted_ciphertext = cipher.decrypt(&mut buf).unwrap();

    assert_eq!(decrypted_ciphertext, plaintext);

    assert_eq!(Alice.shared_secret(&B), Bob.shared_secret(&A));
}
