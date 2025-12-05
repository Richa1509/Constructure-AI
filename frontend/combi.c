#include <stdio.h>

#define MAX_SIZE 10

void generateCombinations(int n, int k, int start, int path[], int pathLen) {
    if (pathLen == k) {
        // Print the combination
        printf("[");
        for (int i = 0; i < k; i++) {
            printf("%d", path[i]);
            if (i < k - 1)
                printf(", ");
        }
        printf("]\n");
        return;
    }
    for (int i = start; i <= n; i++) {
        path[pathLen] = i;
        generateCombinations(n, k, i + 1, path, pathLen + 1);
    }
}

int main() {
    int n = 4;
    int k = 2;
    int path[MAX_SIZE];
    
    generateCombinations(n, k, 1, path, 0);
    
    return 0;
}
