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

#ifndef rtkRayConvexIntersectionImageFilter_hxx
#define rtkRayConvexIntersectionImageFilter_hxx

#include "rtkRayConvexIntersectionImageFilter.h"
#include "rtkProjectionsRegionConstIteratorRayBased.h"

#include <itkImageRegionConstIterator.h>
#include <itkImageRegionIteratorWithIndex.h>

namespace rtk
{

template <class TInputImage, class TOutputImage>
RayConvexIntersectionImageFilter<TInputImage,TOutputImage>
::RayConvexIntersectionImageFilter():
  m_Geometry(nullptr)
{
}

template <class TInputImage, class TOutputImage>
void
RayConvexIntersectionImageFilter<TInputImage,TOutputImage>
::BeforeThreadedGenerateData()
{
  if( this->m_ConvexShape.IsNull() )
    itkExceptionMacro(<<"ConvexShape has not been set.")
}

template <class TInputImage, class TOutputImage>
void
RayConvexIntersectionImageFilter<TInputImage,TOutputImage>
#if ITK_VERSION_MAJOR<5
::ThreadedGenerateData(const OutputImageRegionType& outputRegionForThread,
                       ThreadIdType itkNotUsed(threadId))
#else
::DynamicThreadedGenerateData(const OutputImageRegionType& outputRegionForThread)
#endif
{
  // Iterators on input and output
  using InputRegionIterator = ProjectionsRegionConstIteratorRayBased<TInputImage>;
  InputRegionIterator *itIn;
  itIn = InputRegionIterator::New(this->GetInput(),
                                  outputRegionForThread,
                                  m_Geometry);
  using OutputRegionIterator = itk::ImageRegionIteratorWithIndex<TOutputImage>;
  OutputRegionIterator itOut(this->GetOutput(), outputRegionForThread);

  // Go over each projection
  for(unsigned int pix=0; pix<outputRegionForThread.GetNumberOfPixels(); pix++, itIn->Next(), ++itOut)
    {
    // Compute ray intersection length
    ConvexShape::ScalarType nearDist, farDist;
    if( m_ConvexShape->IsIntersectedByRay(itIn->GetSourcePosition(), itIn->GetDirection(), nearDist, farDist) )
      itOut.Set( itIn->Get() + m_ConvexShape->GetDensity() * ( farDist - nearDist ) );
    else
      itOut.Set( itIn->Get() );
    }

  delete itIn;
}

} // end namespace rtk

#endif
