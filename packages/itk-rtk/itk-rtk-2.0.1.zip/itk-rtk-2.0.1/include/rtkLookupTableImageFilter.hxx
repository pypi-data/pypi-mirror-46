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

#ifndef rtkLookupTableImageFilter_hxx
#define rtkLookupTableImageFilter_hxx

#include "rtkLookupTableImageFilter.h"

namespace rtk
{

template <class TInputImage, class TOutputImage>
void
LookupTableImageFilter<TInputImage, TOutputImage>
::BeforeThreadedGenerateData()
{
  // In case the lut is the result of a pipeline
  this->m_LookupTable->Update();
  this->SetLookupTable( m_LookupTable );
}

}

#endif
