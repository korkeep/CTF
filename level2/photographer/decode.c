#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

uint8_t rotate_left(uint8_t val, uint8_t shift) {
    return (val << shift) | (val >> (8 - shift));
}

uint8_t rotate_right(uint8_t val, uint8_t shift) {
    return (val >> shift) | (val << (8 - shift));
}

int main() {
    FILE *fin = fopen("flag.bmp.enc", "rb");
    if (!fin) {
        perror("failed to open flag.bmp.enc");
        return 1;
    }

    // 파일 크기 측정
    fseek(fin, 0, SEEK_END);
    long size = ftell(fin);
    rewind(fin);

    // 암호화된 데이터 읽기
    uint8_t *enc_data = malloc(size);
    if (fread(enc_data, 1, size, fin) != size) {
        perror("failed to read encrypted file");
        return 1;
    }
    fclose(fin);

    // 복호화 결과 저장할 버퍼
    uint8_t *dec_data = malloc(size);

    // C rand() 초기화
    srand(0xBEEF);

    for (long i = 0; i < size; i++) {
        uint8_t c = enc_data[i];
        int r = rand();
        uint8_t orig;

        switch (i % 3) {
            case 0: {
                // 오른쪽으로 4비트 회전 후, r 하위 8비트 빼고 다시 왼쪽 7비트 회전
                uint8_t v = rotate_right(c, 4);
                v = (v - (r & 0xFF)) & 0xFF;
                orig = rotate_left(v, 7);
                break;
            }
            case 1: {
                // 인코딩 시: rotate_right(orig, shift)
                // 복호화 시: rotate_left(c, shift)
                uint8_t bVar1 = (r >> 31) & 0xFF; // 사실상 항상 0
                int shift = (((r & 0xFF) + (bVar1 >> 5)) & 7) - (bVar1 >> 5);
                orig = rotate_left(c, shift);
                break;
            }
            case 2: {
                orig = ((c + 0x18) & 0xFF) ^ (r & 0xFF);
                break;
            }
        }

        dec_data[i] = orig;
    }

    // 복호화된 결과 저장
    FILE *fout = fopen("flag_decrypted.bmp", "wb");
    if (!fout) {
        perror("failed to open output file");
        return 1;
    }

    fwrite(dec_data, 1, size, fout);
    fclose(fout);

    free(enc_data);
    free(dec_data);

    printf("복호화 완료: flag_decrypted.bmp 생성됨\n");
    return 0;
}
