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

const double PI = 3.1415926f;

struct Circle {
  double x, y, r;

  int resourceCount = 20;                   // 圆的资源被分成几份
  double unitRadian = 2*PI/resourceCount;   // 每份的弧度
  

  void moveCircle(const double angle, const double dist);

  // 得到c2,c所占的弧度, is_main决定谁为主体
  double getRadian(const Circle& c2, const bool& is_main);

  // 得到c2与该c的圆心距离
  double getDistance(const Circle& c2);

  // c2相对于c的角度, is_main决定c是否为主体
  double getDirection(const Circle& c2, const bool& is_main);

};

void Circle::moveCircle(const double angle, const double dist) {
  // 通过已经确定的空间, 与x轴逆时针角度, 距离, 确定下一个空间的位置
  x += cos(angle) * dist;
  y += sin(angle) * dist;
}


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

double Circle::getDirection(const Circle& c2, const bool& is_main) {
  // c2相对于c的角度, is_main决定c是否为主体
  double delta_x, delta_y;
  if (is_main) {
    delta_x = c2.x - this->x;
    delta_y = c2.y - this->y;
  } else {
    delta_x = this->x - c2.x;
    delta_y = this->y - c2.y;
  }

  double alpha = atan(delta_y/delta_x);
  if ((delta_x > 0) && (delta_y > 0)) { return alpha;    // 第一象限
  } else if ((delta_x < 0) && (delta_y > 0)) { return PI+alpha;   // 2
  } else if ((delta_x < 0) && (delta_y < 0)) { return alpha + PI;   // 3
  } else if ((delta_x > 0) && (delta_y < 0)) {return 2*PI+alpha;
  }
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

class ChildrenCircle_lst : public Circle_lst {
 public:
  // ...
  std::vector<std::vector<int> > rsrcIndex_2vec = {};

  // 每个子空间到父空间的距离
  std::vector<double> dist_vec = {};

  std::vector<Circle> childCircles = {};

 private:
  // Circle_lst circles
};


class ParentCircle : public Circle {
 public:
  // 构造函数
  ParentCircle() = default;
  ParentCircle(double p_x, double p_y, double p_r) {
    x = p_x, y = p_y, r = p_r;
  }

  Circle_lst getChildrenClst() {return childrenClst;}

  // 获取父空间到每个子空间的距离
  std::vector<double> getDist_vec();

  // 从子空间获取索引列表
  std::vector<std::vector<int> > getResourceOccupy_2vec();
  


  // 每个资源对应圆的索引列表
  std::vector<std::vector<int> > resourceOccupy_2vec = {};
  ChildrenCircle_lst childrenClst;                  // 对应的所有的子空间
  // 父空间到每个子空间的距离
  std::vector<double> dist_vec = {};
 private:
  
};

// 获取父空间到每个子空间的距离
std::vector<double> ParentCircle::getDist_vec() {
  std::vector<double> vec = {};
  for (int i = 0; i < this->childrenClst.n; i++) {
    double dist = this->getDistance(this->childrenClst.circles[i]);
    vec.push_back(dist);
  }
  this->dist_vec = vec;
  return this->dist_vec;
}

/*
// 从子空间获取索引列表
std::vector<std::vector<int> > ParentCircle::getResourceOccupy_2vec() {
  std::vector<std::vector<int> > vec = {};
  for (int i = 0; i < this->childrenClst.n; i++) {
    vec.push_back(this->childrenClst.childCircles[i].rsrcIndex_vec);
  }
  this->resourceOccupy_2vec = vec;

  return this->resourceOccupy_2vec;
}
*/

class ChildCircle : public Circle {
 public:
  // ParentCircle parentCircle;           // 该子空间的父空间
  // std::vector<int> rsrcIndex_vec = {};     // 子空间占父空间的资源序列
  // 构造函数
  ChildCircle() = default;
  ChildCircle(ParentCircle P, double p_x, double p_y, double p_r) :
      parentCircle(P) {
    // parentCircle = P;
    initResourceIndex();
    x = p_x, y = p_y, r = p_r;
  }
  // 通过parentCircle, rsrcIndex_vec, area, dist生成childCircle
  ChildCircle(ParentCircle P, std::vector<int> r_i_v, double area, double d)
      : parentCircle(P), rsrcIndex_vec(r_i_v) {
    this->r = (sqrt(area/PI));
    this->dist = d;

    // 得到坐标
    reviseCircleFromRsrcIndex(r_i_v);
  }

  // 根据当前数据, 更新子空间
  void updateChildCircle();

  void initResourceIndex() {
    // 当前c对P所占的u弧度
    double radian  = getRadian(parentCircle, false);
    // 当前圆所占资源数量
    int resourceOccupyCount = radian/unitRadian + 1;
    std::cout << "resourceOccupyCount = " << resourceOccupyCount << std::endl;
  }

  ParentCircle getParentCircle() {return parentCircle;}

  // maybe error!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  std::vector<int> getResourceIndex() {return rsrcIndex_vec;}

  int getResourceOccupyCount() {
    // 当前c对P所占的u弧度
    double radian  = getRadian(parentCircle, false);
    // 当前圆所占资源数量
    this->resourceOccupyCount = radian/unitRadian + 1;
    return this->resourceOccupyCount;
  }

  // 得到圆心准确角度
  double getPointAngle();

  // 根据ParentCircle, rsrcIndex_vec, dist, 得到当前circle
  void reviseCircleFromRsrcIndex(std::vector<int>&);
  // 根据当前Circle位置, parentCircle 得到当前rsrcIndex_vec, dist
  void getCircleDataFromParent(ParentCircle new_p);

  ParentCircle parentCircle;     // 该子空间的父空间


  // 每个子空间到父空间的距离
  double dist;

  // 子空间所占父空间资源数量
  int resourceOccupyCount;

  // 子空间所占父空间资源编号
  std::vector<int> rsrcIndex_vec = {};

  // 圆心对应角度
  double pointAngle;

 private:

};

// 得到圆心准确角度
double ChildCircle::getPointAngle() {
  // std::cout << "---- into getPointAngle ---" << std::endl;
  pointAngle = rsrcIndex_vec[0] * unitRadian
      + getRadian(parentCircle, false) / 2;
  return pointAngle;
}

// 根据ParentCircle, rsrcIndex_vec, dist, 得到当前circle
void ChildCircle::reviseCircleFromRsrcIndex(std::vector<int>& vec) {
  // vec = {0, 1, 2};
  this->rsrcIndex_vec = vec;
  double angle = getPointAngle();
  // std::cout << "angle = " << angle << std::endl;
  // std::cout << this->x << " " << this->y << " " << this->r << std::endl;
  this->x = this->parentCircle.x + cos(angle) * dist;
  this->y = this->parentCircle.y + sin(angle) * dist;
  // std::cout << this->x << " " << this->y << " " << this->r << std::endl;
}

// 根据当前Circle位置, parentCircle 得到当前rsrcIndex_vec, dist
void ChildCircle::getCircleDataFromParent(ParentCircle new_P) {
  // std::cout << "---- into getCircleDataFromParent() ----" << std::endl;
  // 当前P修改为新父空间
  this->parentCircle = new_P;

  std::vector<int> new_rsrcVec = {};
  double angle = getDirection(this->parentCircle, false);
  int first_i = angle / this->unitRadian;
  for (int i = 0; i < this->resourceOccupyCount; i++) {
    // std::cout << first_i << " ";
    new_rsrcVec.push_back(first_i++);
  }
  // std::cout << std::endl;
  // 更新资源列表
  this->rsrcIndex_vec = new_rsrcVec;
  // 修改距离

  this->dist = getDistance(parentCircle);
  // std::cout << "dist = " << this->dist << std::endl;
  // std::cout << "---- end getCircleDataFromParent() ----" << std::endl;
}



