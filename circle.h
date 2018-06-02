 /*  ------------------------------
    Copyright <2018> [Tim Hu]
    email: timtingwei@hotamail.com    
   ------------------------------
   File:circle.h
   Date:Sat Jun  2 14:12:22 CST 2018
   compile: g++ -std=c++11 spaceOrder.cpp -lGLEW -lGL -lGLU -lglfw3 -lX11 -lXxf86vm -lXrandr -lpthread -lXi -ldl -lXinerama -lXcursor
   -----------------------------
*/

#include <iostream>
#include <vector>

// const double PI = 3.1415926f;

struct Circle {
  double x, y, r;

  const int resourceCount = 20;             // 圆的资源被分成几份

  double unitRadian = 2*PI/resourceCount;   // 每份的弧度

  void moveCircle(const double angle, const double dist);

  // 得到c2,c所占的弧度, is_main决定谁为主体
  double getRadian(const Circle& c2, const bool& is_main);

  // 得到c2与该c的圆心距离
  double getDistance(const Circle& c2);
};

double Circle::getRadian(const Circle& c2, const bool& is_main) {
  // 得到c2,c所占的弧度, is_main决定谁为主体
  double dist = getDistance(c2);
  // is_main, true, c2占c1; false, c1占c2
  double area = (is_main) ? (pow(c2.r, 2)*PI): pow(r, 2)*PI;
  return 2 * atan(sqrt(area/PI)/dist);
}

double Circle::getDistance(const Circle& c2) {
  // 得到c2与该c的圆心距离
  double dist = sqrt(pow((x - c2.x), 2) +
                    (pow((y - c2.y), 2)));
  return dist;
}


struct Circle_lst {
  Circle circles[50];
  int n = 0;
  Circle coverCircle;

  void appendCircle(Circle);
  void appendCircles(Circle_lst);
  void getCoverCircle();
  void moveCircles(double angle, double dist);
  Circle getFarthestCircle(const Circle P);

  void printCircles();
  void drawCircles(int childrenColor);
};

struct Circle_tree {
  Circle_lst clsts_arr[50];
  int n = 0;

  void appendClst(Circle_lst);

  void printTreeCircles();
};

class ParentCircle : public Circle {
 public:
  // 构造函数
  ParentCircle() = default;
  ParentCircle(double p_x, double p_y, double p_r) {
    x = p_x, y = p_y, r = p_r;
  }

  Circle_lst getChildrenClst() {return _childrenClst;}

  // 
 private:
  const int _resourceCount = 20;             // 等分成20份资源
  std::vector<int> _resourceOccupy_vec = {};     // 每个资源对应圆的索引列表
  Circle_lst _childrenClst;                  // 对应的所有的子空间
};

class ChildCircle : public Circle {
 public:
  // ParentCircle parentCircle;           // 该子空间的父空间
  // std::vector<int> rsrcIndex = {};     // 子空间占父空间的资源序列
  // 构造函数
  ChildCircle() = default;
  ChildCircle(ParentCircle P, double p_x, double p_y, double p_r) :
      _parentCircle(P) {
    // _parentCircle = P;
    x = p_x, y = p_y, r = p_r;
  }

  void initResourceIndex() {
    // 当前c对P所占的u弧度
    double radian  = getRadian(_parentCircle, false);
    // 当前圆所占资源数量
    int resource_count = radian/unitRadian + 1;
    std::cout << "resource_count = " << resource_count << std::endl;
  }

  ParentCircle getParentCircle() {return _parentCircle;}

  std::vector<int> getResourceIndex() {return _rsrcIndex;}

 private:
  ParentCircle _parentCircle;     // 该子空间的父空间
  std::vector<int> _rsrcIndex = {};     // 子空间占父空间的资源序列
};

class ChildrenCircle_lst : public Circle_lst {
 public:
  // ...
 private:
  // Circle_lst circles
  std::vector<std::vector<int> > _rsrcIndex_vec = {};
};
