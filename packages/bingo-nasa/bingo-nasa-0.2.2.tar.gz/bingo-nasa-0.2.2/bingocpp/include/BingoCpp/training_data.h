/*!
 * \file training_data.h
 *
 * \author Ethan Adams
 * \date
 *
 * This file contains the cpp version of training_data.py
 *
 * Copyright 2018 United States Government as represented by the Administrator 
 * of the National Aeronautics and Space Administration. No copyright is claimed 
 * in the United States under Title 17, U.S. Code. All Other Rights Reserved.
 *
 * The Bingo Mini-app platform is licensed under the Apache License, Version 2.0 
 * (the "License"); you may not use this file except in compliance with the 
 * License. You may obtain a copy of the License at  
 * http://www.apache.org/licenses/LICENSE-2.0. 
 *
 * Unless required by applicable law or agreed to in writing, software 
 * distributed under the License is distributed on an "AS IS" BASIS, WITHOUT 
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the 
 * License for the specific language governing permissions and limitations under 
 * the License.
 */

#ifndef INCLUDE_BINGOCPP_TRAINING_DATA_H_
#define INCLUDE_BINGOCPP_TRAINING_DATA_H_

#include <Eigen/Dense>
#include <Eigen/Core>
#include <vector>
#include <list>


namespace bingo {

/*! \struct TrainingData
 *
 *  An abstract struct to hold the data for fitness calculations
 *
 *  \note TrainingData includes : Implicit and Explicit data
 *
 *  \fn TrainingData* get_item(std::list<int> items)
 *  \fn int size()
 */
struct TrainingData {
 public:
  TrainingData() { }
  /*! \brief gets a new training data with certain rows
  *
  *  \param[in] items The rows to retrieve. std::list<int>
  *  \return TrainingData* with the selected data
  */
  virtual TrainingData* get_item(std::list<int> items) = 0;
  /*! \brief gets the size of x
  *
  *  \return int the amount of rows in x
  */
  virtual int size() = 0;
};

/*! \struct ExplicitTrainingData
 *  \brief This struct holds data for Explicit regression.
 */
struct ExplicitTrainingData : TrainingData {
 public:
  ExplicitTrainingData() : TrainingData() { }
  //! Eigen::ArrayXXd x
  /*! x variabes for ExplicitTraining */
  Eigen::ArrayXXd x;
  //! Eigen::ArrayXXd y
  /*! y variabes for ExplicitTraining */
  Eigen::ArrayXXd y;
  //! \brief Constructor
  ExplicitTrainingData(Eigen::ArrayXXd vx, Eigen::ArrayXXd vy);
  ExplicitTrainingData* get_item(std::list<int> items);
  int size() {
    return x.rows();
  }
};

/*! \struct ImplicitTrainingData
 *  \brief This struct holds data for Implicit regression.
 */
struct ImplicitTrainingData : TrainingData {
 public:
  ImplicitTrainingData() : TrainingData() { }
  //! Eigen::ArrayXXd x
  /*! x variabes for ImplicitTraining */
  Eigen::ArrayXXd x;
  //! Eigen::ArrayXXd dx_dt
  /*! dx_dt variabes for ImplicitTraining */
  Eigen::ArrayXXd dx_dt;
  //! \brief Constructor
  ImplicitTrainingData(Eigen::ArrayXXd vx);
  //! \brief Constructor
  ImplicitTrainingData(Eigen::ArrayXXd vx, Eigen::ArrayXXd vdx_dt);
  ImplicitTrainingData* get_item(std::list<int> items);
  int size() {
    return x.rows();
  }
};
} // namespace bingo
#endif
