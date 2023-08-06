/*=========================================================================
 *
 *  Copyright RTK Consortium
 *
 *  Licensed under the Apache License, Version 2.0 (the "License");
 *  you may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at
 *
 *         http://www.apache.org/licenses/LICENSE-2.0.txt
 *
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *  limitations under the License.
 *
 *=========================================================================*/

#ifndef rtkNesterovUpdateImageFilter_h
#define rtkNesterovUpdateImageFilter_h

#include "itkInPlaceImageFilter.h"

namespace rtk
{

/** \class NesterovUpdateImageFilter
 * \brief Applies Nesterov's momentum technique
 *
 * NesterovUpdateImageFilter implements Nesterov's momentum technique
 * in order to accelerate the convergence rate of Newton's method, or
 * other optimization algorithms. The first input is the current iterate,
 * the second input is the product of the inverse hessian matrix
 * by the gradient vector (the Newton's update, before applying a minus sign)
 *
 * \author Cyril Mory
 *
 * \ingroup RTK
*/

template< typename TImage>
class NesterovUpdateImageFilter : public itk::InPlaceImageFilter< TImage,  TImage>
{
public:
  ITK_DISALLOW_COPY_AND_ASSIGN(NesterovUpdateImageFilter);

  /** Standard class type alias. */
  using Self = NesterovUpdateImageFilter;
  using Superclass = itk::InPlaceImageFilter< TImage, TImage>;
  using Pointer = itk::SmartPointer< Self >;

  /** Convenient type alias */
  using OutputImageRegionType = typename Superclass::OutputImageType::RegionType;

  /** Method for creation through the object factory. */
  itkNewMacro(Self)

  /** Run-time type information (and related methods). */
  itkTypeMacro(NesterovUpdateImageFilter, itk::InPlaceImageFilter)

  /** Get and Set macro*/
  itkGetMacro(NumberOfIterations, int)
  itkSetMacro(NumberOfIterations, int)

protected:
  NesterovUpdateImageFilter();
  ~NesterovUpdateImageFilter() override;

  /** Does the real work. */
  void BeforeThreadedGenerateData() override;
#if ITK_VERSION_MAJOR<5
  void ThreadedGenerateData(const OutputImageRegionType& outputRegionForThread, itk::ThreadIdType itkNotUsed(threadId)) override;
#else
  void DynamicThreadedGenerateData(const OutputImageRegionType& outputRegionForThread) override;
#endif
  void AfterThreadedGenerateData() override;

  void GenerateInputRequestedRegion() override;

  int                                   m_NumberOfIterations;
  int                                   m_CurrentIteration;
  bool                                  m_MustInitializeIntermediateImages;
  typename TImage::PixelType::ValueType m_tCoeff;
  typename TImage::PixelType::ValueType m_tCoeffNext;
  typename TImage::PixelType::ValueType m_Sum;
  typename TImage::PixelType::ValueType m_Ratio;

  // Internal images
  typename TImage::Pointer m_Vk;
  typename TImage::Pointer m_Alphak;

};
} //namespace RTK


#ifndef ITK_MANUAL_INSTANTIATION
#include "rtkNesterovUpdateImageFilter.hxx"
#endif

#endif
