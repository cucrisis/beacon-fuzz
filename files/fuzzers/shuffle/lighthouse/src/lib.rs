use std::{mem, ptr, slice};
use swap_or_not_shuffle::shuffle_list;

#[no_mangle]
pub extern "C" fn shuffle_list_c(
    input_ptr: *mut usize,
    input_size: usize,
    seed_ptr: *const u8,
) -> bool {
    assert_eq!(
        mem::size_of::<usize>(),
        mem::size_of::<u64>(),
        "Other implementations return u64"
    );

    let input: &[usize] = unsafe { slice::from_raw_parts(input_ptr, input_size as usize) };

    let seed: &[u8] = unsafe { slice::from_raw_parts(seed_ptr, 32) };

    return match shuffle_list(input.to_vec(), 90, &seed, false) {
        None => false,
        Some(x) => {
            unsafe {
                ptr::copy_nonoverlapping(x.as_ptr(), input_ptr, input_size);
            }
            true
        }
    };
}
