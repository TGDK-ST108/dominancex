#include <iostream>
#include <fstream>
#include <openssl/evp.h>
#include <cstring>
std::string decrypt(const std::string& encrypted, const std::string& key) {
    EVP_CIPHER_CTX *ctx = EVP_CIPHER_CTX_new();
    unsigned char k[32] = {0};
    strncpy((char*)k, key.c_str(), sizeof(k));
    std::string output;
    unsigned char outbuf[1024];
    int outlen;
    EVP_DecryptInit_ex(ctx, EVP_aes_256_ecb(), NULL, k, NULL);
    EVP_DecryptUpdate(ctx, outbuf, &outlen, (const unsigned char*)encrypted.data(), encrypted.size());
    output.assign((char*)outbuf, outlen);
    EVP_DecryptFinal_ex(ctx, outbuf, &outlen);
    output.append((char*)outbuf, outlen);
    EVP_CIPHER_CTX_free(ctx);
    return output;
}
int main(int argc, char** argv) {
    std::ifstream f(argv[1], std::ios::binary);
    std::string line;
    std::string key = "QQUAp";
    while (std::getline(f, line)) {
        std::string result = decrypt(line, key);
        std::cout << result << std::endl;
    }
    return 0;
}
