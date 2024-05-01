#include <stdio.h>
#include <stdlib.h>
#include <string.h>
void errorCheck(FILE *file1, FILE *file2, char *argv[]) {
  if (!file1) {
    printf("Couldn't open '%s'.\nExiting\n", argv[1]);
    exit(0);
  }
  if (!file2) {
    printf("Couldn't open '%s'.\nExiting\n", argv[2]);
    exit(0);
  }
}
// void print_rest_of_file(FILE
void read(FILE *file1, FILE *file2) {
  char *line_buf1 = NULL;
  char *line_buf2 = NULL;
  size_t line_buf_size1 = 0;
  size_t line_buf_size2 = 0;
  unsigned int line_count = 0;
  ssize_t line_size1 = getline(&line_buf1, &line_buf_size1, file1);
  ssize_t line_size2 = getline(&line_buf2, &line_buf_size2, file2);
  unsigned int error_count = 0;
  while (line_size1 >= 0 && line_size2 >= 0) {
    line_count++;
    if (strcmp(line_buf1, line_buf2) != 0) {
      printf("[%06u]:\n%s%s", line_count, line_buf1, line_buf2);
      error_count++;
    }

    line_size1 = getline(&line_buf1, &line_buf_size1, file1);
    line_size2 = getline(&line_buf2, &line_buf_size2, file2);
  }
  if (line_size1 > 0 || line_size2 > 0) {
    printf("one file is bigger than the other.\n");
  }
  if (error_count == 0) {
    printf("==========================\nTexts are identical");
  } else {
    printf("==========================\nNumber of errors:%u\nIgnore this if its the last line(todo:fix)\n", error_count);
  }
  free(line_buf1);
  free(line_buf2);
}
int main(int argc, char *argv[]) {
  if (argc != 3) {
    // case where out input in more than 2 compare files
    printf("Incorrect number of files.\n");
    return 0;
  }
  FILE *file1 = fopen(argv[1], "r");
  FILE *file2 = fopen(argv[2], "r");
  errorCheck(file1, file2, argv);
  read(file1, file2);

  fclose(file1);
  fclose(file2);
  return 0;
}
