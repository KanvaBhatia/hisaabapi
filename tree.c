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

N insert(N, int);
void inorder(N);
void preorder(N);
void postorder(N);
N findSmallest(N);
N findLargest(N);
void search(N, int);
int totalNodes(N);
int height(N);
int totalInternal(N);
int totalExternal(N);
N deleteElement(N, int);
N delete(N);


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

N findSmallest(N tree){
    if(tree -> llink == NULL){
        return tree;
    }
    tree = findSmallest(tree -> llink);
    return tree;

}

N findLargest(N tree){
    if(tree == NULL || tree -> rlink == NULL){
        return tree;
    }
    tree = findLargest(tree -> rlink);
    return tree;

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

int totalNodes(N tree){
    if(tree == NULL)
        return 0;
    return totalNodes(tree -> llink) + totalNodes(tree -> rlink) + 1;
}

int height(N tree){
    if(tree == NULL)
        return 0;
    int left = height(tree -> llink);
    int right = height(tree -> rlink);
    if(left > right)
    return left + 1;
    return right + 1;
}

int totalInternal(N tree){
    if(tree == NULL)
        return 0;
    if(tree -> llink == NULL && tree -> rlink == NULL)
        return 0;
    return totalInternal(tree -> llink) + totalInternal(tree -> rlink) + 1;
}

int totalExternal(N tree){
    if(tree == NULL)
        return 0;
    if(tree -> llink == NULL && tree -> rlink == NULL)
        return 1;
    return totalExternal(tree -> llink) + totalExternal(tree -> rlink); 
}

N deleteElement(N tree, int key){
    if(tree == NULL){
        printf("Key not found!\n");
        return tree;
    }
    if(key < tree -> data)
        tree -> llink = deleteElement(tree -> llink, key);
    else if(key > tree -> data)
        tree -> rlink = deleteElement(tree -> rlink, key);
    else{
        if(tree -> rlink != NULL && tree -> llink != NULL){
            N succ = tree -> rlink;
            while(succ -> llink)
                succ = succ -> llink;
            tree -> data = succ -> data;
            tree -> rlink = deleteElement(tree -> rlink, succ -> data);
        }else{
            if(tree -> llink)
                tree = tree -> llink;
            else if(tree -> rlink)
                tree = tree -> rlink;
            else
                tree = NULL;
        }
    }
    return tree;    
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

    N smallest = findSmallest(tree);
    printf("\nsmallest = %d\n", smallest -> data);
    N largest = findLargest(tree);
    printf("\nlargest = %d\n", largest -> data);
    
    search(tree, 97);
    printf("\nTotal nodes - %d\n", totalNodes(tree));
    printf("\nHeight - %d\n", height(tree));
    printf("\nTotal internal - %d\n", totalInternal(tree));
    printf("\nTotal External - %d\n", totalExternal(tree));

    deleteElement(tree, 200);
    deleteElement(tree, 31);
    deleteElement(tree, 90);
    deleteElement(tree, 431);
    inorder(tree);


}


// 3 80 90 91 92 93 100 110 150 175 200 250 ---- 3 80 90 91 92 93 100 110 150 175 200 250
// 93 3 80 90 91 92 100 110 150 175 200 250 ---- 93 91 3 90 80 92 200 150 110 100 175 250 
// 3 80 90 91 92 100 110 150 175 200 250 93 ---- 80 90 3 92 91 100 110 175 150 250 200 93  