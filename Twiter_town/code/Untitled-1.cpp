#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

const long long MOD = 998244353;

long long maxProductMod(const vector<int>& digits) {
    vector<int> sortedDigits(digits);
    sort(sortedDigits.rbegin(), sortedDigits.rend());

    long long num1 = 0, num2 = 0;
    for (size_t i = 0; i < sortedDigits.size(); ++i) {
        if (i % 2 == 0) {
            num1 = (num1 * 10 + sortedDigits[i]) % MOD;
        } else {
            num2 = (num2 * 10 + sortedDigits[i]) % MOD;
        }
    }

    return (num1 * num2) % MOD;
}

int main() {
    // Subproblem 1
    vector<int> digits1 = {4, 9, 5, 4, 6, 8, 3, 9, 5, 7, 9, 1, 1, 7, 6, 5, 9};
    cout << "Subproblem 1 - Maximum product modulo 998244353: " << maxProductMod(digits1) << endl;

    // Subproblem 2
    vector<int> digits2 = {6, 1, 5, 8, 1, 7, 7, 8, 7, 4, 7, 5, 5, 4, 3, 1, 5, 9, 3, 8, 7, 1, 6, 7, 9, 4, 2, 3, 4, 1, 6, 5, 5, 5, 9, 7, 5, 4, 9, 3, 2, 5, 2, 8, 9, 1, 5, 8, 4, 4, 6, 2, 3, 7, 6, 5, 5, 7, 8, 7, 6, 5, 4, 6, 8, 3, 1, 1, 5, 6, 6, 2, 1, 1, 7, 2, 8, 8, 8, 9, 8, 3, 9, 1, 5, 5, 3, 8, 9, 5, 3, 7, 5, 3, 6, 7, 2, 6, 1, 6};
    cout << "Subproblem 2 - Maximum product modulo 998244353: " << maxProductMod(digits2) << endl;

    return 0;
}
