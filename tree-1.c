#include <stdio.h>

#include <stdlib.h>
#include <string.h>
#include <math.h>

struct node
{
    int data;
    struct node* rlink;
    struct node* llink;
};

typedef struct node* N;

N insert(N tree, int value){
    if(tree == NULL){
        tree = (N)malloc(sizeof(struct node));
        tree -> data = value;
        tree -> rlink = NULL;
        tree -> llink = NULL;
        return tree;
    }
    if(value < tree -> data){
        tree -> llink = insert(tree -> llink, value);}
    else if(value > tree -> data){
        tree -> rlink = insert(tree -> rlink, value);}
    else{
        printf("Element already in tree!\n");}
    return tree;
}

void inorder(N tree){
    if(tree != NULL){
        inorder(tree -> llink);
        printf("%d ", tree -> data);
        inorder(tree -> rlink);
    }else{return;}
}
void preorder(N tree){
    if(tree != NULL){
        printf("%d ", tree -> data);
        preorder(tree -> llink);
        preorder(tree -> rlink);
    }else{return;}
}
void postorder(N tree){
    if(tree != NULL){
        postorder(tree -> llink);
        postorder(tree -> rlink);
        printf("%d ", tree -> data);
    }else{return;}
}

void search(N tree, int key){
    if(tree == NULL)
        printf("Key not found!");
    else if(tree -> data == key)
        printf("Key found!");
    else if(key < tree -> data)
        search(tree -> llink, key);
    else if(key > tree -> data)
        search(tree -> rlink, key);
}

int main(){
    N tree = NULL;
    tree = insert(tree, 93);
    tree = insert(tree, 200);
    tree = insert(tree, 150);
    tree = insert(tree, 110);
    tree = insert(tree, 91);
    tree = insert(tree, 175);
    tree = insert(tree, 3);
    tree = insert(tree, 100);
    tree = insert(tree, 90);
    tree = insert(tree, 92);
    tree = insert(tree, 250);
    tree = insert(tree, 80);
    inorder(tree);
    printf("\n");
    preorder(tree);
    printf("\n");
    postorder(tree);
    printf("\n");
}