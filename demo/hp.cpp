#include <iostream>
#ifdef _WIN32
#include <process.h>
#else
#include <unistd.h>
#endif
using namespace std;


int hp = 100;
int main()
{
    int pid = (int) getpid();
    cout<< "PID:" << pid << endl;
    int t; 
    cout<< "Size of HP: " << sizeof(hp) << endl;
    while (1){
        cout << "Currently your HP equals " << hp << "." << endl;
        cout << "Input a number to add it: ";
        cin >> t;
        hp += t;
    }
    return 0;
}
